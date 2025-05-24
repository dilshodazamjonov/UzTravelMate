from django.urls import path
from .views import *

app_name = 'friend'

urlpatterns = [
    path('friend_requests_list/', friend_requests_view, name='friend_requests_list'),
    path('list/', friends_list_view, name='friends-list'),
    path('request/send/', send_friend_request_view, name='send-friend-request'),
    path("request/accept/", accept_friend_request_view, name="accept-friend-request"),
    path('request/decline/', decline_friend_request_view, name='decline-friend-request'),
    path('request/cancel/', cancel_friend_request_view, name='cancel-friend-request'),
    path('remove/', remove_friend_view, name='remove-friend'),

    path('search-users/', search_users, name='search-users'),
]