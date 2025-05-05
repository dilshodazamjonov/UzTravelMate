from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

@admin.register(Account)
class AccountAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'username', 'date_joined', 'last_login', 'is_active', 'is_staff']
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Персональная информация'), {'fields': ('profile_image', 'hide_email')}),
        (_('Права доступа'), {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')


@admin.register(TravelerProfile)
class TravelerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'top_destination')
    search_fields = ('user__username', 'user__email', 'top_destination')
    list_filter = ('top_destination',)
    raw_id_fields = ('user',)


@admin.register(AgencyProfile)
class AgencyProfileAdmin(admin.ModelAdmin):
    list_display = ('agency_name', 'user', 'location', 'website')
    search_fields = ('agency_name', 'user__username', 'location')
    list_filter = ('location',)
    raw_id_fields = ('user',)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('agency', 'destination', 'trip_date', 'price')
    list_filter = ('agency', 'trip_date')
    search_fields = ('agency__agency_name', 'destination')
    ordering = ('-trip_date',)

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code')





