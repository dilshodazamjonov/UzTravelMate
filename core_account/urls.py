from django.urls import path
from .views import *


app_name = 'core_account'

urlpatterns = [
    path('profile/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/edit/', TravelerProfileView.as_view(), name='traveler-profile'),

    path('password-reset/', send_password_reset_email),
    path('password-reset-confirm/', reset_password_confirm),
    path('all-users/', get_user_identifiers, name='all_users'),

    path('location/', user_location_view, name='user-location'),
    path('nearby_users/', nearby_users_view, name='nearby-users')
]
