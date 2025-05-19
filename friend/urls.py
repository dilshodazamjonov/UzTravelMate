from django.urls import path
from .views import *

app_name = 'friend'

urlpatterns = [
    path('send-friend-request/', send_friend_request_view, name='send-friend-request'),
]