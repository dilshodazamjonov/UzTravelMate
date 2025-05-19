from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.utils.dateparse import parse_date
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from account.models import Account, EmailVerification
import json
import random

User = get_user_model()

def generate_verification_code():
    return str(random.randint(100000, 999999))

@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST allowed'}, status=405)

    if request.user.is_authenticated:
        return JsonResponse({'message': f'Вы уже вошли как {request.user.username.upper()}'}, status=400)

    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return JsonResponse({'message': 'Необходимо указать email и пароль'}, status=400)

    try:
        EmailValidator()(email)
    except ValidationError:
        return JsonResponse({'message': 'Неверный формат email'}, status=400)

    try:
        user = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return JsonResponse({'message': 'Пользователь с таким email не найден'}, status=404)

    user = authenticate(request, username=email, password=password)
    if user:
        login(request, user)
        return JsonResponse({'message': 'Вы успешно вошли в систему'}, status=200)
    return JsonResponse({'message': 'Неверный email или пароль'}, status=401)

@csrf_exempt
def logout_view(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST allowed'}, status=405)
    logout(request)
    return JsonResponse({'message': 'Вы успешно вышли из системы'})

@csrf_exempt
def register_view(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST allowed'}, status=405)

    if request.user.is_authenticated:
        return JsonResponse({'message': f'Вы уже зарегистрированы как {request.user.username.upper()}'}, status=400)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        dob_str = data.get('date_of_birth')

        if not all([email, username, password, password_confirm]):
            return JsonResponse({'message': 'Пожалуйста, заполните все поля'}, status=400)
        if password != password_confirm:
            return JsonResponse({'message': 'Пароли не совпадают'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Этот email уже зарегистрирован'}, status=400)

        user = User.objects.create_user(email=email, username=username, password=password)
        user.is_active = False
        user.user_type = 'traveler'
        user.save()

        dob = parse_date(dob_str) if dob_str else None
        if dob:
            user.travelerprofile.date_of_birth = dob
            user.travelerprofile.save()

        code = generate_verification_code()
        EmailVerification.objects.create(user=user, code=code)

        send_mail(
            'Код подтверждения UzTravelMate',
            f'Ваш код подтверждения: {code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'Код подтверждения отправлен на указанный email'}, status=201)

    except Exception as e:
        return JsonResponse({'message': f'Ошибка: {str(e)}'}, status=500)

@csrf_exempt
def verify_code_view(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST allowed'}, status=405)

    if request.user.is_authenticated:
        return JsonResponse({'message': f'Вы уже подтвердили email как {request.user.username.upper()}'}, status=400)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')

        if not email or not code:
            return JsonResponse({'message': 'Необходимо указать email и код подтверждения'}, status=400)

        user = User.objects.get(email=email)
        verification = EmailVerification.objects.get(user=user)

        if verification.code == code:
            user.is_active = True
            user.save()
            verification.delete()
            return JsonResponse({'message': 'Email успешно подтвержден! Теперь вы можете войти.'})
        else:
            return JsonResponse({'message': 'Неверный код подтверждения'}, status=400)

    except EmailVerification.DoesNotExist:
        return JsonResponse({'message': 'Код подтверждения не найден или уже использован'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'message': 'Пользователь не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'message': f'Ошибка: {str(e)}'}, status=500)




