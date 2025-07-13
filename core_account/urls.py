from django.urls import path
from core_account.views import (
    TravelerProfileView,
    RecommendedUsersView,
    SendPasswordResetEmailView,
    ResetPasswordConfirmView,
    UserDetailView,
    AllUsersEmails,
    UserLocationView,
    NearbyUsersView,
    ProfileCompletionCheckView,
    TravelChoicesView
)

app_name = 'core_account'

urlpatterns = [
    path("users/<str:username>/", UserDetailView.as_view(), name="user-detail"),
    path("profiles/<str:email>/", TravelerProfileView.as_view(), name="traveler-profile"),

    # Resetting the password
    path("reset-password/", SendPasswordResetEmailView.as_view(), name="reset-password"),
    path("reset-password-confirm/<uidb64>/<token>/", ResetPasswordConfirmView.as_view(), name="reset-password-confirm"),

    # Fetching profile info
    path("usernames/", AllUsersEmails.as_view(), name="usernames"),
    path("profiles/<str:email>/is-complete/", ProfileCompletionCheckView.as_view(), name="profile-complete-check"),
    path("travel-choices/", TravelChoicesView.as_view(), name="travel-choices"),
    
    # recommendation and location endpoints
    path("location/", UserLocationView.as_view(), name="user-location"),
    path("nearby-users/", NearbyUsersView.as_view(), name="nearby-users"),
    path("recommended/", RecommendedUsersView.as_view(), name="recommended-users"),
]