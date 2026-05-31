import logging
from datetime import timedelta

from django.utils.timezone import now

from FarmManager.constants import MessageTemplates, MessageTypes
from FarmManager.models import Message, Reproduction

from .sendMesage import send_alert

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEAT_ALERT_CYCLE_DAYS = 20
HEAT_ALERT_DUE_REMAINDERS = (0, 1)


def is_heat_alert_due(heat_sign_start, today=None):
    """Return whether a heat reminder is due and the days since heat started."""
    if not heat_sign_start:
        return False, None

    today = today or now().date()
    days_since_last_heat = (today - heat_sign_start.date()).days
    is_due = (
        days_since_last_heat >= HEAT_ALERT_CYCLE_DAYS
        and days_since_last_heat % HEAT_ALERT_CYCLE_DAYS
        in HEAT_ALERT_DUE_REMAINDERS
    )
    return is_due, days_since_last_heat


def _heat_alert_sent_today(farm, cow, message_text, today):
    return Message.objects.filter(
        farm=farm,
        cow=cow,
        message_type=MessageTypes.HEAT_MONITORING_ALERT,
        message_text=message_text,
        is_sent=True,
        sent_date__date=today,
    ).exists()


def _send_due_heat_alert(
    phone_number,
    message_text,
    cow_reproduction,
    today,
    recipient_label,
    dry_run=False,
):
    if _heat_alert_sent_today(
        cow_reproduction.farm, cow_reproduction.cow, message_text, today
    ):
        logger.info(
            "Heat monitoring alert already sent today for Cow %s to %s",
            cow_reproduction.cow.cow_id,
            recipient_label,
        )
        return False

    if dry_run:
        logger.info(
            "[DRY RUN] Would send heat monitoring alert for Cow %s to %s",
            cow_reproduction.cow.cow_id,
            recipient_label,
        )
        return True

    try:
        alert_response = send_alert(phone_number, message_text)
    except Exception as exc:
        logger.exception(
            "Failed to send heat alert for Cow %s to %s: %s",
            cow_reproduction.cow.cow_id,
            recipient_label,
            exc,
        )
        return False

    if alert_response.get("status") == "success":
        Message.objects.create(
            farm=cow_reproduction.farm,
            cow=cow_reproduction.cow,
            message_text=message_text,
            message_type=MessageTypes.HEAT_MONITORING_ALERT,
            is_sent=True,
        )
        logger.info(
            "Heat monitoring alert sent for Cow %s to %s",
            cow_reproduction.cow.cow_id,
            recipient_label,
        )
        return True

    logger.error(
        "Failed to send heat alert for Cow %s to %s: %s",
        cow_reproduction.cow.cow_id,
        recipient_label,
        alert_response.get("message") or alert_response.get("response"),
    )
    return False


def check_heat_sign_alerts(dry_run=False):
    """Checks non-pregnant cows for heat sign alerts and sends notifications if necessary"""
    today = now().date()
    alert_count = 0

    # Get cows that are NOT pregnant
    cows = Reproduction.objects.select_related(
        "farm", "cow", "farm__inseminator"
    ).filter(is_cow_pregnant=False)

    for cow_reproduction in cows:
        is_due, days_since_last_heat = is_heat_alert_due(
            cow_reproduction.heat_sign_start, today
        )
        if not is_due:
            continue

        last_heat_date = cow_reproduction.heat_sign_start.strftime("%Y-%m-%d")
        farmer_message = MessageTemplates.heat_monitoring_reminder(
            cow_reproduction.cow.cow_id,
            days_since_last_heat,
            last_heat_date,
        )

        if _send_due_heat_alert(
            cow_reproduction.farm.telephone_number,
            farmer_message,
            cow_reproduction,
            today,
            "farmer",
            dry_run=dry_run,
        ):
            alert_count += 1

        inseminator = cow_reproduction.farm.inseminator
        if not inseminator:
            logger.warning(
                "No inseminator assigned for Farm %s; skipped inseminator heat alert for Cow %s",
                cow_reproduction.farm.farm_id,
                cow_reproduction.cow.cow_id,
            )
            continue

        if not inseminator.is_active:
            logger.warning(
                "Inactive inseminator assigned for Farm %s; skipped inseminator heat alert for Cow %s",
                cow_reproduction.farm.farm_id,
                cow_reproduction.cow.cow_id,
            )
            continue

        inseminator_message = MessageTemplates.heat_monitoring_inseminator_reminder(
            cow_reproduction.farm.farm_id,
            cow_reproduction.farm.owner_name,
            cow_reproduction.farm.telephone_number,
            cow_reproduction.cow.cow_id,
            days_since_last_heat,
            last_heat_date,
        )

        if _send_due_heat_alert(
            inseminator.phone_number,
            inseminator_message,
            cow_reproduction,
            today,
            "inseminator",
            dry_run=dry_run,
        ):
            alert_count += 1

    logger.info(
        f"Heat sign check complete: {alert_count} alerts sent out of {len(cows)} non-pregnant cows"
    )
    action = "would send" if dry_run else "sent"
    return (
        f"Checked {len(cows)} non-pregnant cows, {action} "
        f"{alert_count} heat monitoring alerts"
    )


def check_pregnancy_alerts():
    """Checks pregnant cows for calving alerts (2 months, 1 month, and due date)"""
    today = now().date()
    alert_count = 0

    # Get pregnant cows with expected calving dates
    pregnant_cows = Reproduction.objects.filter(
        is_cow_pregnant=True, calving_date__isnull=False
    )

    for cow_reproduction in pregnant_cows:
        expected_calving_date = cow_reproduction.calving_date
        days_until_calving = (expected_calving_date - today).days

        # Determine which alert to send based on days until calving
        alert_type = None
        message_template = None

        if 58 <= days_until_calving <= 62:  # 2 months (around 60 days)
            alert_type = MessageTypes.CALVING_2_MONTHS_ALERT
            message_template = MessageTemplates.calving_2_months_alert
        elif 28 <= days_until_calving <= 32:  # 1 month (around 30 days)
            alert_type = MessageTypes.CALVING_1_MONTH_ALERT
            message_template = MessageTemplates.calving_1_month_alert
        elif -2 <= days_until_calving <= 2:  # Due date (±2 days)
            alert_type = MessageTypes.CALVING_DUE_ALERT
            message_template = MessageTemplates.calving_due_alert

        if alert_type and message_template:
            # Check if we already sent this type of alert for this cow
            existing_alert = Message.objects.filter(
                farm=cow_reproduction.farm,
                cow=cow_reproduction.cow,
                message_type=alert_type,
                sent_date__gte=today - timedelta(days=7),  # Within last 7 days
            ).exists()

            if not existing_alert:
                # Create the alert message
                message_text = message_template(
                    cow_reproduction.cow.cow_id,
                    expected_calving_date.strftime("%Y-%m-%d"),
                    cow_reproduction.cow.lactation_number or 1,
                )

                # Send alert first
                alert_response = send_alert(
                    cow_reproduction.farm.telephone_number, message_text
                )

                # Create message record only if alert was sent successfully
                if alert_response.get("status") == "success":
                    Message.objects.create(
                        farm=cow_reproduction.farm,
                        cow=cow_reproduction.cow,
                        message_text=message_text,
                        message_type=alert_type,
                        is_sent=True,
                    )
                    alert_count += 1

                    alert_description = {
                        MessageTypes.CALVING_2_MONTHS_ALERT: "2-month calving reminder",
                        MessageTypes.CALVING_1_MONTH_ALERT: "1-month calving reminder",
                        MessageTypes.CALVING_DUE_ALERT: "calving due date alert",
                    }

                    logger.info(
                        f"✅ {alert_description[alert_type]} sent for Cow {cow_reproduction.cow.cow_id} "
                        f"(due in {days_until_calving} days)"
                    )
                else:
                    logger.error(
                        f"❌ Failed to send pregnancy alert for Cow {cow_reproduction.cow.cow_id}: "
                        f"{alert_response.get('message')}"
                    )

    logger.info(
        f"Pregnancy check complete: {alert_count} alerts sent out of {len(pregnant_cows)} pregnant cows"
    )
    return f"Checked {len(pregnant_cows)} pregnant cows, sent {alert_count} pregnancy alerts"


def run_daily_checks():
    """Run all daily monitoring checks"""
    logger.info("🔄 Starting daily farm monitoring checks...")

    # Run heat sign alerts for non-pregnant cows
    heat_result = check_heat_sign_alerts()

    # Run pregnancy monitoring alerts for pregnant cows
    pregnancy_result = check_pregnancy_alerts()

    logger.info("✅ Daily farm monitoring checks completed")
    logger.info(f"📊 Summary - Heat: {heat_result} | Pregnancy: {pregnancy_result}")

    return f"Daily checks completed - {heat_result} | {pregnancy_result}"
