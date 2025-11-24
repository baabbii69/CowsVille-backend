from django.db.models import Count, Q
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Cow, Farm


@receiver(post_save, sender=Cow)
@receiver(post_delete, sender=Cow)
def update_farm_counts(sender, instance, **kwargs):
    """
    Update Farm statistics whenever a Cow is added, updated, or deleted.
    """
    farm = instance.farm
    # Calculate new stats
    # We filter by is_deleted=False because we only want active cows
    all_active_cows = Cow.objects.filter(farm=farm, is_deleted=False)
    # 1. Total Cows
    total_cows = all_active_cows.count()
    farm.total_number_of_cows = total_cows
    # 2. Milking Cows
    # Logic: Cows with average_daily_milk > 0 are considered milking
    milking_cows = all_active_cows.filter(average_daily_milk__gt=0).count()
    farm.number_of_milking_cows = milking_cows
    # 3. Calves (Optional placeholder)
    # farm.number_of_calves = ...
    farm.save()


# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.db.models import Sum, Count
# from .models import Cow, Farm
# @receiver(post_save, sender=Cow)
# @receiver(post_delete, sender=Cow)
# def update_farm_counts(sender, instance, **kwargs):
#     """
#     Update Farm statistics whenever a Cow is added, updated, or deleted.
#     """
#     farm = instance.farm

#     # Calculate new stats
#     all_cows = Cow.objects.filter(farm=farm, is_deleted=False)

#     total_cows = all_cows.count()
#     milking_cows = all_cows.filter(status='Lactating').count() # Adjust 'status' field name if different
#     # If 'status' is not the field, maybe check 'is_milking' or similar based on your model
#     # Based on your model, you might need to check:
#     # number_of_milking_cows = all_cows.filter(lactation_number__gt=0).count()
#     # OR check if you have a specific status field.
#     # Assuming 'number_of_milking_cows' logic:

#     # Let's try to infer milking status.
#     # If you don't have a direct status field, you might need to rely on other logic.
#     # For now, we will just update the total count which is the most critical.

#     farm.total_number_of_cows = total_cows

#     # Update other counts if possible
#     # farm.number_of_milking_cows = ...
#     # farm.number_of_calves = ...

#     farm.save()
