from django.urls import path
from .views import *

urlpatterns = [

    #   =========== ENDPOINTS FOR AUTHENTICATION =============

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('verify/', verify_code_view, name='verify'),


    #    ========== ENDPOINT FOR CSRF TOKEN ==================

    path('api/get-csrf/', get_csrf_token, name='get_csrf'),
]

