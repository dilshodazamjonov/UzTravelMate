from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from .models import *
from .utils import save_google_profile_image


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



@receiver(user_signed_up)
def handle_social_signup(request, user, **kwargs):

    if user.socialaccount_set.exists():
        user.is_active = True
        user.save()

        try:
            social_account = SocialAccount.objects.get(user=user, provider='google')
            picture_url = social_account.extra_data.get('picture')

            if picture_url:
                save_google_profile_image(user, picture_url)
        except SocialAccount.DoesNotExist:
            print("[SIGNAL] No Google social account found.")
