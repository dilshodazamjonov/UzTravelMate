from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, TravelerProfile, AgencyProfile

@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'traveler':
            TravelerProfile.objects.create(user=instance)
        elif instance.user_type == 'agency':
            AgencyProfile.objects.create(user=instance)
