from django.urls import path
from .views import (
    FriendRequestReceivedListView,
    SendFriendRequestView,
    AcceptFriendRequestView,
    DeclineFriendRequestView,
    CancelFriendRequestView,
    FriendsListView,
    RemoveFriendView,
    SearchUsersView,
)

app_name = 'friend'

urlpatterns = [
    # Friend requests
    path('requests/received/', FriendRequestReceivedListView.as_view(), name='friend-requests-received'),  # GET
    path('requests/send/', SendFriendRequestView.as_view(), name='friend-request-send'),                   # POST
    path('requests/accept/', AcceptFriendRequestView.as_view(), name='friend-request-accept'),             # POST
    path('requests/decline/', DeclineFriendRequestView.as_view(), name='friend-request-decline'),          # POST
    path('requests/cancel/', CancelFriendRequestView.as_view(), name='friend-request-cancel'),             # POST

    # Friends
    path('friends/', FriendsListView.as_view(), name='friend-list'),                                        # GET
    path('friends/remove/', RemoveFriendView.as_view(), name='friend-remove'),                             # POST

    # ============== Search =================
    path('users/search/', SearchUsersView.as_view(), name='user-search'),                                   # GET
]
