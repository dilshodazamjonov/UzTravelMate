from django.urls import path
from .views import *


app_name = 'account'

urlpatterns = [
    path('profile/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('profile/edit/', TravelerProfileView.as_view(), name='traveler-profile'),

    path('password-reset/', send_password_reset_email),
    path('password-reset-confirm/', reset_password_confirm),
]
