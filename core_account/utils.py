from allauth.socialaccount.models import SocialAccount
import requests
from django.core.files.base import ContentFile

def get_google_profile_picture(user):
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        picture_url = social_account.extra_data.get('picture')
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
