from django.contrib import admin
from .models import (
    Interest,
    TravelerInterest,
    TravelerPreferences,
    DestinationRecommendation,
)


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    verbose_name = "Интерес"
    verbose_name_plural = "Интересы"


@admin.register(TravelerInterest)
class TravelerInterestAdmin(admin.ModelAdmin):
    list_display = ("traveler", "interest")
    search_fields = ("traveler__user__username", "interest__name")
    list_filter = ("interest",)
    autocomplete_fields = ("traveler", "interest")
    verbose_name = "Интерес путешественника"
    verbose_name_plural = "Интересы путешественников"


@admin.register(TravelerPreferences)
class TravelerPreferencesAdmin(admin.ModelAdmin):
    list_display = (
        "traveler",
        "travel_style",
        "top_destination",
        "budget_level",
        "travel_start_date",
        "travel_end_date",
    )
    list_filter = ("travel_style", "budget_level")
    search_fields = ("traveler__user__username", "top_destination")
    autocomplete_fields = ("traveler",)
    verbose_name = "Предпочтения путешественника"
    verbose_name_plural = "Предпочтения путешественников"


@admin.register(DestinationRecommendation)
class DestinationRecommendationAdmin(admin.ModelAdmin):
    list_display = ("traveler", "destination", "score", "created_at")
    search_fields = ("traveler__user__username", "destination")
    list_filter = ("created_at",)
    ordering = ("-score",)
    autocomplete_fields = ("traveler",)
    verbose_name = "Рекомендация направления"
    verbose_name_plural = "Рекомендации направлений"
