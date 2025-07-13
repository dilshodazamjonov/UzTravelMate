# core_account/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from core_account.models import EmailVerification
from django.core.mail import send_mail
from django.conf import settings
import random
from core_account.models import TravelerProfile
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

User = get_user_model()

def generate_verification_code():
    return str(random.randint(100000, 999999))

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот email уже зарегистрирован")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password']

        user = User.objects.create_user(email=email, username=username, password=password)
        user.is_active = False
        user.user_type = 'traveler'
        user.save()

        code = generate_verification_code()
        EmailVerification.objects.create(user=user, code=code)

        send_mail(
            'Код подтверждения UzTravelMate',
            f'Ваш код подтверждения: {code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return user

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            verification = EmailVerification.objects.get(user=user)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("Код подтверждения не найден или уже использован")

        if verification.code != data['code']:
            raise serializers.ValidationError("Неверный код подтверждения")

        data['user'] = user
        data['verification'] = verification
        return data

    def save(self):
        user = self.validated_data['user']
        verification = self.validated_data['verification']

        user.is_active = True
        user.save()
        verification.delete()

        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'email': user.email,
            'username': user.username,
        }





# core_account/serializers.py (add this below the previous serializers)



User = get_user_model()

class GoogleOneTapSerializer(serializers.Serializer):
    credential = serializers.CharField()

    def validate(self, data):
        CLIENT_ID = '748489865467-0jmbqd6atd49se8ct23j3jctkhkitug0.apps.googleusercontent.com'
        token = data['credential']

        try:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)
        except ValueError:
            raise serializers.ValidationError("Invalid Google ID token")

        email = idinfo.get('email')
        name = idinfo.get('name')
        picture = idinfo.get('picture')

        if not email:
            raise serializers.ValidationError("Email not provided in token")

        data['email'] = email
        data['name'] = name
        data['picture'] = picture
        data['sub'] = idinfo.get('sub')
        return data

    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data.get('name')
        picture = validated_data.get('picture')

        try:
            user = User.objects.get(email=email)
            created = False
        except User.DoesNotExist:
            base_username = email.split('@')[0]
            username = base_username
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{uuid.uuid4().hex[:6]}"

            user = User.objects.create(
                email=email,
                username=username,
                is_active=True,
                user_type='traveler'
            )
            created = True

        if name and not user.username:
            user.username = name

        if picture and hasattr(user, 'profile_image'):
            user.profile_image = picture  # Make sure your field can accept URL or handle separately

        user.is_active = True
        user.save()

        if user.user_type == 'traveler':
            TravelerProfile.objects.get_or_create(user=user)

        refresh = RefreshToken.for_user(user)

        return {
            'created': created,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'email': user.email,
            'username': user.username,
            'user_type': user.user_type,
            'profile_image': str(user.profile_image),
        }
