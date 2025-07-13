from django.db.models.signals import post_save
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from .models import Account, TravelerProfile, AgencyProfile
from .utils import save_google_profile_image


@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'traveler':
            TravelerProfile.objects.create(user=instance)
        elif instance.user_type == 'agency':
            AgencyProfile.objects.create(user=instance)


@receiver(user_signed_up)
def handle_social_signup(request, user, **kwargs):

    if user.socialaccount_set.exists():
        user.is_active = True
        user.save()

        try:
            social_account = SocialAccount.objects.get(user=user, provider='google')
            picture_url = social_account.extra_data.get('picture') # type: ignore

            if picture_url:
                save_google_profile_image(user, picture_url)
        except SocialAccount.DoesNotExist:
            print("[SIGNAL] No Google social account found.")
