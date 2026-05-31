from django.core.management.base import BaseCommand

from AlertSystem.updater import check_heat_sign_alerts


class Command(BaseCommand):
    help = "Check non-pregnant cows for due heat sign alerts."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview due heat alerts without sending SMS or creating messages.",
        )

    def handle(self, *args, **options):
        result = check_heat_sign_alerts(dry_run=options["dry_run"])
        self.stdout.write(self.style.SUCCESS(result))
