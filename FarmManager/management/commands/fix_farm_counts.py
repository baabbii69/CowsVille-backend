from django.core.management.base import BaseCommand
from FarmManager.models import Farm, Cow
class Command(BaseCommand):
    help = 'Recalculates total cow counts for all farms'
    def handle(self, *args, **kwargs):
        for farm in Farm.objects.all():
            count = Cow.objects.filter(farm=farm, is_deleted=False).count()
            farm.total_number_of_cows = count
            farm.save()
            self.stdout.write(f"Updated Farm {farm.farm_id}: {count} cows")