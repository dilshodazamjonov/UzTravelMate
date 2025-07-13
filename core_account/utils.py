from allauth.socialaccount.models import SocialAccount
import requests
from datetime import timedelta
from django.core.files.base import ContentFile

def get_google_profile_picture(user: SocialAccount):
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        picture_url = social_account.extra_data.get('picture') # type: ignore
        return picture_url
    except SocialAccount.DoesNotExist:
        return None



def save_google_profile_image(user, image_url):
    if not image_url:
        return

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            file_name = f"profile_image_{user.pk}.png"
            user.profile_image.save(file_name, ContentFile(response.content), save=True)
        else:
            print("[save_google_profile_image] Failed to fetch image")
    except Exception as e:
        print(f"[save_google_profile_image] Error: {e}")


def recommend_travelers(user_profile):
    from .models import TravelerProfile

    if not user_profile.is_profile_complete():
        return TravelerProfile.objects.none()

    candidates = TravelerProfile.objects.exclude(user=user_profile.user)

    # Match destination
    candidates = candidates.filter(top_destination=user_profile.top_destination)

    # Match budget
    candidates = candidates.filter(budget_level=user_profile.budget_level)

    # Match travel style
    candidates = candidates.filter(travel_style__overlap=user_profile.travel_style)

    # Match travel date overlap
    candidates = candidates.filter(
        travel_start_date__lte=user_profile.travel_end_date + timedelta(days=3),
        travel_end_date__gte=user_profile.travel_start_date - timedelta(days=3),
    )

    return candidates
