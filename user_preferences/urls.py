from django.urls import path
from user_preferences.views import InterestListView, TravelDestinationsListView, PreferencesChoicesView

app_name = "user_preferences"

urlpatterns = [
    path('interests/', InterestListView.as_view(), name='interest-list'),
    path("travel-destinations/", TravelDestinationsListView.as_view(), name="travel-destinations"),
    path("preferences-choices/", PreferencesChoicesView.as_view(), name='preferences-choices')
]