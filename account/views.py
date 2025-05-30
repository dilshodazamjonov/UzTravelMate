from rest_framework.authentication import BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAuthenticatedOrReadOnly
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
import json
from friend.auth import CsrfExemptSessionAuthentication
from friend.utils import get_nearby_users
from .serializers import *



class UserDetailView(RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(Account, username=username)

    def get_serializer_context(self):
        return {'request': self.request}


@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
class TravelerProfileView(RetrieveUpdateAPIView):
    serializer_class = TravelerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.travelerprofile

@csrf_exempt
def send_password_reset_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://localhost:3000/reset-password-confirm/{uid}/{token}/"

        send_mail(
            subject='Reset Your Password',
            message=f"Click this link to reset your password: {reset_link}",
            from_email=None,
            recipient_list=[email],
        )

        return JsonResponse({'message': 'Password reset email sent'})
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)



@csrf_exempt
def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except Exception:
        return Response({'error': 'Invalid UID'}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

    new_password = request.data.get('new_password')
    if not new_password:
        return Response({'error': 'New password required'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])  # Use IsAuthenticated if needed
def get_user_identifiers(request):
    users = Account.objects.all()
    result = []

    for user in users:
        if user.username:
            result.append(user.username)

    return Response(result)



@api_view(['GET', 'PUT', 'POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_location_view(request):
    user = request.user

    location, _ = UserLocation.objects.get_or_create(user=user)

    if request.method == 'GET':
        serializer = UserLocationSerializer(location)
        return Response(serializer.data)

    elif request.method in ['PUT', 'POST']:
        serializer = UserLocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def nearby_users_view(request):
    current_user = request.user
    radius_km = request.query_params.get('radius_km', 100)
    try:
        radius_km = float(radius_km)
    except ValueError:
        radius_km = 50

    nearby_users = get_nearby_users(current_user, radius_km)

    serializer = AccountSerializer(nearby_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
