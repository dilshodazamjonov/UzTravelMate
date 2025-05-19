from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'traveler':
            TravelerProfile.objects.create(user=instance)
        elif instance.user_type == 'agency':
            AgencyProfile.objects.create(user=instance)

@receiver(post_save, sender=TravelerProfile)
def update_profile_completed(sender, instance, **kwargs):
    user = instance.user
    if all([instance.date_of_birth, instance.interests, instance.travel_style, instance.top_destination]):
        user.profile_completed = True
    else:
        user.profile_completed = False
    user.save()
