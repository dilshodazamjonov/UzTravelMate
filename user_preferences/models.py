from django.db import models
from core_account.models import TravelerProfile


class Interest(models.Model):
    name = models.CharField("Название интереса", max_length=50, unique=True)

    class Meta:
        verbose_name = "Интерес"
        verbose_name_plural = "Интересы"

    def __str__(self):
        return self.name


class TravelerInterest(models.Model):
    traveler = models.ForeignKey(
        TravelerProfile,
        on_delete=models.CASCADE,
        related_name="traveler_interests",
        verbose_name="Путешественник"
    )
    interest = models.ForeignKey(
        Interest,
        on_delete=models.CASCADE,
        verbose_name="Интерес"
    )

    class Meta:
        unique_together = ("traveler", "interest")
        verbose_name = "Интерес путешественника"
        verbose_name_plural = "Интересы путешественников"

    def __str__(self):
        return f"{self.traveler.user.username} — {self.interest.name}"


class TravelDestinations(models.Model):
    name = models.CharField(verbose_name="Название направления", max_length=100)
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Направление путешествия"
        verbose_name_plural = "Направления путешествий"

    def __str__(self):
        return self.name

class TravelerPreferences(models.Model):
    traveler = models.OneToOneField(
        TravelerProfile,
        on_delete=models.CASCADE,
        related_name="preferences",
        verbose_name="Путешественник"
    )

    travel_style = models.CharField(
        "Стиль путешествия",
        max_length=20,
        choices=[
            ('solo', 'Один'),
            ('group', 'Группой'),
            ('adventure', 'Приключения'),
            ('relax', 'Отдых'),
            ('local', 'Местная жизнь'),
        ],
        null=True, blank=True
    )

    top_destination = models.ForeignKey(
        TravelDestinations, on_delete=models.SET_NULL,
        related_name="preferred_by",
        verbose_name="Любимое направление",
        blank=True, null=True
    )

    travel_start_date = models.DateField(verbose_name="Дата начала поездки", null=True, blank=True)
    travel_end_date = models.DateField(verbose_name="Дата окончания поездки", null=True, blank=True)

    budget_level = models.CharField(
        verbose_name="Бюджет",
        max_length=10,
        choices=[
            ('low', 'Низкий'),
            ('mid', 'Средний'),
            ('high', 'Высокий')
        ],
        null=True, blank=True
    )

    class Meta:
        verbose_name = "Предпочтения путешественника"
        verbose_name_plural = "Предпочтения путешественников"

    def __str__(self):
        return f"Предпочтения {self.traveler.user.username}"


class DestinationRecommendation(models.Model):
    traveler = models.ForeignKey(
        TravelerProfile,
        on_delete=models.CASCADE,
        verbose_name="Путешественник"
    )
    destination = models.CharField("Рекомендуемое направление", max_length=100)
    reason = models.TextField("Причина рекомендации", blank=True, null=True)
    score = models.FloatField("Релевантность", default=0.0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Рекомендация направления"
        verbose_name_plural = "Рекомендации направлений"

    def __str__(self):
        return f"{self.destination} для {self.traveler.user.username}"
