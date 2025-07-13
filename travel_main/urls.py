from django.urls import path
from .views import (
    
    RegisterAPIView,
    VerifyCodeAPIView, 
    GoogleOneTapLoginAPIView
    )
    
urlpatterns = [

    #   =========== ENDPOINTS FOR AUTHENTICATION =============

    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/verify/', VerifyCodeAPIView.as_view(), name='verify'),
    path('api/google-login/', GoogleOneTapLoginAPIView.as_view(), name='google_login'),

]

