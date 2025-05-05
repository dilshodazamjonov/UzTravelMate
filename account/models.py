from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse


# Менеджер пользовательской модели
class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('У пользователя должен быть адрес электронной почты')
        if not username:
            raise ValueError('У пользователя должно быть имя пользователя')

        user = self.model(
            email=self.normalize_email(email),
            username=username
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


# Путь к файлу изображения профиля
def get_profile_image_filepath(self, filename):
    return f'profile_image/{self.pk}/profile_image.png'


# Изображение по умолчанию
def get_default_profile_image():
    return 'UzTravelMate/dummy_image.png'


# Кастомная модель пользователя
class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=60, unique=True, db_index=True, verbose_name='Электронная почта'
    )
    username = models.CharField(
        max_length=30, unique=True, verbose_name='Имя пользователя'
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата регистрации'
    )
    last_login = models.DateTimeField(
        auto_now=True, verbose_name='Последний вход'
    )
    is_admin = models.BooleanField(
        default=False, verbose_name='Администратор'
    )
    is_active = models.BooleanField(
        default=True, verbose_name='Активен'
    )
    is_staff = models.BooleanField(
        default=False, verbose_name='Персонал'
    )
    is_superuser = models.BooleanField(
        default=False, verbose_name='Суперпользователь'
    )
    profile_image = models.ImageField(
        max_length=255,
        upload_to=get_profile_image_filepath,
        null=True,
        blank=True,
        default=get_default_profile_image,
        verbose_name='Изображение профиля'
    )
    hide_email = models.BooleanField(
        default=True, verbose_name='Скрыть email'
    )

    def get_display_email(self):
        if self.hide_email:
            return "Email Hidden"
        return self.email

    USER_TYPE_CHOICES = (
        ('traveler', 'Traveler'),
        ('agency', 'Travel Hosting Agency'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, db_index=True, default='traveler')

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return self.username

    def get_profile_image_filename(self):
        try:
            return str(self.profile_image)[str(self.profile_image).index(f'profile_image/{self.pk}/'):]
        except ValueError:
            return str(self.profile_image)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # def get_absolute_url(self):
    #     return reverse('admin:account_account_change', args=[self.pk])


class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TravelerProfile(Profile):
    date_of_birth = models.DateField(null=True, blank=True)
    interests = models.JSONField(default=list, blank=True)
    travel_style = models.JSONField(default=list, blank=True)
    top_destination = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Traveler Profile"

    class Meta:
        verbose_name = "Профиль путешественника"
        verbose_name_plural = "Профили путешественников"


# AgencyProfile model
class AgencyProfile(Profile):
    agency_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.agency_name

    class Meta:
        verbose_name = "Профиль агентства"
        verbose_name_plural = "Профили агентств"


class Trip(models.Model):
    agency = models.ForeignKey(AgencyProfile, on_delete=models.CASCADE, related_name='trips')
    destination = models.CharField(max_length=100)
    trip_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Trip to {self.destination} on {self.trip_date}"

    class Meta:
        verbose_name = "Поездка"
        verbose_name_plural = "Поездки"

from django.conf import settings

class EmailVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification for {self.user.email}"









