from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from django.utils.html import format_html


# ---------------------- #
# Custom User Manager    #
# ---------------------- #
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('У пользователя должен быть адрес электронной почты')
        if not username:
            raise ValueError('У пользователя должно быть имя пользователя')

        user = self.model(
            email=self.normalize_email(email),
            username=username.lower()  # Ensuring username is lowercase
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# ---------------------- #
# Helper for Profile Img #
# ---------------------- #
def get_profile_image_filepath(instance, filename):
    return f'profile_image/{instance.pk}/profile_image.png'

def get_default_profile_image():
    return 'defaults/profile_default.png'  # Updated to a more intuitive path

# ---------------------- #
# Custom User Model      #
# ---------------------- #
class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True, db_index=True, verbose_name='Электронная почта')
    username = models.CharField(max_length=30, unique=True, verbose_name='Имя пользователя')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    last_login = models.DateTimeField(auto_now=True, verbose_name='Последний вход')
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')
    is_active = models.BooleanField(default=False, verbose_name='Активен')  # Default set to False to ensure verification
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')
    hide_email = models.BooleanField(default=True, verbose_name='Скрыть email')

    profile_image = models.ImageField(
        max_length=255,
        upload_to=get_profile_image_filepath,
        null=True,
        blank=True,
        default=get_default_profile_image,
        verbose_name='Изображение профиля'
    )


    USER_TYPE_CHOICES = (
        ('traveler', 'Traveler'),
        ('agency', 'Travel Hosting Agency'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, db_index=True, default='traveler')

    profile_completed = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return self.username

    def get_display_email(self):
        return "Email Hidden" if self.hide_email else self.email

    def get_profile_image(self):
        return format_html('<img src="{}" width="60" height="60" style="object-fit: cover;" />',
                           self.profile_image.url)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



# ---------------------- #
# Traveler Profile       #
# ---------------------- #
def default_interests():
    return []

def default_travel_style():
    return []

class TravelerProfile(models.Model):
    profile_image = models.ImageField(
        max_length=255,
        upload_to=get_profile_image_filepath,
        null=True,
        blank=True,
        default=get_default_profile_image,
        verbose_name='Изображение профиля'
    )
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    interests = models.JSONField(default=default_interests, blank=True)
    travel_style = models.JSONField(default=default_travel_style, blank=True)
    top_destination = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Traveler Profile"

    class Meta:
        verbose_name = "Профиль путешественника"
        verbose_name_plural = "Профили путешественников"

    def get_profile_image_filename(self):
        try:
            return str(self.profile_image)[str(self.profile_image).index(f'profile_image/{self.pk}/'): ]
        except ValueError:
            return str(self.profile_image)

    def is_profile_complete(self):
        return all([
            self.date_of_birth,
            self.interests,
            self.travel_style,
            self.top_destination,
        ])

    def save(self, *args, **kwargs):
        # Update the Account's profile image if TravelerProfile's image is set
        if self.profile_image:
            self.user.profile_image = self.profile_image
            self.user.save()
        super().save(*args, **kwargs)


# ---------------------- #
# Agency Profile         #
# ---------------------- #
class AgencyProfile(models.Model):
    profile_image = models.ImageField(
        max_length=255,
        upload_to=get_profile_image_filepath,
        null=True,
        blank=True,
        default=get_default_profile_image,
        verbose_name='Изображение профиля'
    )
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    agency_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.agency_name

    class Meta:
        verbose_name = "Профиль агентства"
        verbose_name_plural = "Профили агентств"


# ---------------------- #
# Email Verification     #
# ---------------------- #
class EmailVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, db_index=True)  # Added db_index for performance
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=15)

    def __str__(self):
        return f"Verification for {self.user.email}"

class UserLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='location')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Location of {self.user.username}"