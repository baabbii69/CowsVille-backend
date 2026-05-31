from datetime import date, datetime, timedelta
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from AlertSystem.updater import check_heat_sign_alerts, is_heat_alert_due

from .models import (
    BreedType,
    Cow,
    Farm,
    FeedingFrequency,
    FloorType,
    GynecologicalStatus,
    HousingType,
    Inseminator,
    Message,
    Reproduction,
    WaterSource,
)


class HeatAlertScheduleTests(TestCase):
    def test_heat_alert_is_due_on_day_20_and_21_of_each_cycle(self):
        heat_start = timezone.make_aware(datetime(2026, 1, 1, 8, 0))
        start_date = date(2026, 1, 1)

        due_offsets = [20, 21, 40, 41, 60, 61]
        not_due_offsets = [0, 18, 19, 22, 23, 39, 42]

        for offset in due_offsets:
            is_due, days_since_heat = is_heat_alert_due(
                heat_start, start_date + timedelta(days=offset)
            )
            self.assertTrue(is_due, f"Expected day {offset} to be due")
            self.assertEqual(days_since_heat, offset)

        for offset in not_due_offsets:
            is_due, days_since_heat = is_heat_alert_due(
                heat_start, start_date + timedelta(days=offset)
            )
            self.assertFalse(is_due, f"Expected day {offset} not to be due")
            self.assertEqual(days_since_heat, offset)

    def test_heat_alert_is_not_due_without_heat_start(self):
        is_due, days_since_heat = is_heat_alert_due(None, date(2026, 1, 21))

        self.assertFalse(is_due)
        self.assertIsNone(days_since_heat)


class HeatAlertUpdaterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.housing_type = HousingType.objects.create(
            name="test_housing", display_name="Test Housing"
        )
        cls.floor_type = FloorType.objects.create(
            name="test_floor", display_name="Test Floor"
        )
        cls.feeding_frequency = FeedingFrequency.objects.create(
            name="test_feeding", display_name="Test Feeding"
        )
        cls.water_source = WaterSource.objects.create(
            name="test_water", display_name="Test Water"
        )
        cls.breed_type = BreedType.objects.create(
            name="test_breed", display_name="Test Breed"
        )
        cls.gynecological_status = GynecologicalStatus.objects.create(
            name="test_status", display_name="Test Status"
        )
        cls.inseminator = Inseminator.objects.create(
            name="Test Inseminator",
            phone_number="+251911111111",
            address="Addis Ababa",
            is_active=True,
        )

    def setUp(self):
        self.farm = Farm.objects.create(
            farm_id="FARM001",
            owner_name="Test Farmer",
            address="Test Address",
            telephone_number="+251912345678",
            fertility_camp_no=1,
            total_number_of_cows=1,
            number_of_calves=0,
            number_of_milking_cows=1,
            total_daily_milk=10,
            type_of_housing=self.housing_type,
            type_of_floor=self.floor_type,
            main_feed="Hay",
            rate_of_cow_feeding=self.feeding_frequency,
            source_of_water=self.water_source,
            rate_of_water_giving=self.feeding_frequency,
            farm_hygiene_score=3,
            inseminator=self.inseminator,
        )
        self.cow = Cow.objects.create(
            farm=self.farm,
            cow_id="COW001",
            breed=self.breed_type,
            sex=Cow.Gender.FEMALE,
            body_weight=350,
            bcs=3.0,
            gynecological_status=self.gynecological_status,
            lactation_number=1,
            days_in_milk=30,
            average_daily_milk=8,
        )
        self.fixed_now = timezone.now().replace(
            hour=9, minute=0, second=0, microsecond=0
        )
        self.heat_start = self.fixed_now - timedelta(days=20)

    def create_reproduction(self, **overrides):
        defaults = {
            "farm": self.farm,
            "cow": self.cow,
            "heat_sign_start": self.heat_start,
            "is_cow_pregnant": False,
        }
        defaults.update(overrides)
        return Reproduction.objects.create(**defaults)

    @patch("AlertSystem.updater.send_alert")
    @patch("AlertSystem.updater.now")
    def test_due_alert_sends_to_farmer_and_inseminator_once_per_day(
        self, mock_now, mock_send_alert
    ):
        mock_now.return_value = self.fixed_now
        mock_send_alert.return_value = {"status": "success"}
        self.create_reproduction()

        result = check_heat_sign_alerts()

        self.assertIn("sent 2 heat monitoring alerts", result)
        self.assertEqual(mock_send_alert.call_count, 2)
        self.assertEqual(Message.objects.count(), 2)

        sent_numbers = {call.args[0] for call in mock_send_alert.call_args_list}
        self.assertEqual(
            sent_numbers, {self.farm.telephone_number, self.inseminator.phone_number}
        )

        mock_send_alert.reset_mock()
        result = check_heat_sign_alerts()

        self.assertIn("sent 0 heat monitoring alerts", result)
        mock_send_alert.assert_not_called()
        self.assertEqual(Message.objects.count(), 2)

    @patch("AlertSystem.updater.send_alert")
    @patch("AlertSystem.updater.now")
    def test_dry_run_command_does_not_send_sms_or_create_messages(
        self, mock_now, mock_send_alert
    ):
        mock_now.return_value = self.fixed_now
        self.create_reproduction()
        output = StringIO()

        call_command("check_heat_signs", "--dry-run", stdout=output)

        mock_send_alert.assert_not_called()
        self.assertEqual(Message.objects.count(), 0)
        self.assertIn("would send 2 heat monitoring alerts", output.getvalue())

    @patch("AlertSystem.updater.send_alert")
    @patch("AlertSystem.updater.now")
    def test_pregnant_cows_are_skipped(self, mock_now, mock_send_alert):
        mock_now.return_value = self.fixed_now
        self.create_reproduction(is_cow_pregnant=True)

        result = check_heat_sign_alerts()

        self.assertIn("sent 0 heat monitoring alerts", result)
        mock_send_alert.assert_not_called()
        self.assertEqual(Message.objects.count(), 0)

    @patch("AlertSystem.updater.send_alert")
    @patch("AlertSystem.updater.now")
    def test_inactive_inseminator_does_not_block_farmer_alert(
        self, mock_now, mock_send_alert
    ):
        mock_now.return_value = self.fixed_now
        mock_send_alert.return_value = {"status": "success"}
        self.inseminator.is_active = False
        self.inseminator.save()
        self.create_reproduction()

        result = check_heat_sign_alerts()

        self.assertIn("sent 1 heat monitoring alerts", result)
        self.assertEqual(mock_send_alert.call_count, 1)
        self.assertEqual(mock_send_alert.call_args.args[0], self.farm.telephone_number)
        self.assertEqual(Message.objects.count(), 1)
