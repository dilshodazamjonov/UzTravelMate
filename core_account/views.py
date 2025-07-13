from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import default_token_generator

from friend.utils import get_nearby_users
from .utils import recommend_travelers
from .serializers import AccountSerializer, TravelerProfileSerializer, UserLocationSerializer
from .models import Account, TravelerProfile, UserLocation
from user_preferences.models import TravelerPreferences



class UserDetailView(RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self): # type: ignore
        username = self.kwargs.get('username')
        return get_object_or_404(Account, username=username)

    def get_serializer_context(self):
        return {'request': self.request}




class TravelerProfileView(APIView):
    permission_classes = []

    @swagger_auto_schema(responses={200: TravelerProfileSerializer})
    def get(self, request, email):
        user = get_object_or_404(Account, email=email)
        profile = TravelerProfile.objects.filter(user=user).first()

        if not profile:
            return Response({"detail": "Traveler profile not found."}, status=404)

        serializer = TravelerProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TravelerProfileSerializer)
    def put(self, request, email):
        return self._update_profile(request, email)

    @swagger_auto_schema(request_body=TravelerProfileSerializer)
    def patch(self, request, email):
        return self._update_profile(request, email, partial=True)

    def _update_profile(self, request, email, partial=False):
        user = get_object_or_404(Account, email=email)
        if request.user != user:
            return Response({"detail": "You are not allowed to modify another user's profile."}, status=403)

        profile = TravelerProfile.objects.filter(user=user).first()
        if not profile:
            return Response({"detail": "Traveler profile not found."}, status=404)

        serializer = TravelerProfileSerializer(profile, data=request.data, partial=partial, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendedUsersView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: TravelerProfileSerializer(many=True)})
    def get(self, request):
        matches = recommend_travelers(request.user.travelerprofile)
        serializer = TravelerProfileSerializer(matches, many=True, context={'request': request})
        return Response(serializer.data)


class SendPasswordResetEmailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email'],
        properties={'email': openapi.Schema(type=openapi.TYPE_STRING)}))
    def post(self, request):
        email = request.data.get('email')
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"https://travelpair.vercel.app/reset-password-confirm/{uid}/{token}/"

        send_mail(
            subject='Reset Your Password',
            message=f"Click this link to reset your password: {reset_link}",
            from_email=None,
            recipient_list=[email],
        )

        return Response({'message': 'Password reset email sent'})


class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['new_password'],
        properties={'new_password': openapi.Schema(type=openapi.TYPE_STRING)}))
    def post(self, request, uidb64, token):
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

        return Response({'message': 'Password has been reset successfully.'})


class AllUsersEmails(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of emails",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING)
                )
            )
        }
    )
    def get(self, request):
        emails = list(Account.objects.exclude(email='').values_list('email', flat=True))
        return Response(emails)

class UserLocationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserLocationSerializer})
    def get(self, request):
        location, _ = UserLocation.objects.get_or_create(user=request.user)
        serializer = UserLocationSerializer(location)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserLocationSerializer)
    def put(self, request):
        location, _ = UserLocation.objects.get_or_create(user=request.user)
        serializer = UserLocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserLocationSerializer)
    def post(self, request):
        return self.put(request)


class NearbyUsersView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('radius_km', openapi.IN_QUERY, description="Radius in kilometers", type=openapi.TYPE_NUMBER)
    ])
    def get(self, request):
        try:
            radius_km = float(request.query_params.get('radius_km', 100))
        except ValueError:
            radius_km = 50

        nearby_users = get_nearby_users(request.user, radius_km) # type: ignore
        serializer = AccountSerializer(nearby_users, many=True)
        return Response(serializer.data)


class ProfileCompletionCheckView(APIView):
    @swagger_auto_schema(
        operation_description="Check if the traveler's profile and preferences are complete.",
        responses={200: "Returns {'is_complete': true/false}"}
    )
    def get(self, request, email):
        user = get_object_or_404(Account, email=email)
        profile = TravelerProfile.objects.filter(user=user).first()

        if not profile:
            return Response({"is_complete": False, "reason": "Traveler profile not found."}, status=200)

        preferences = getattr(profile, 'preferences', None)

        profile_complete = bool(profile.date_of_birth and profile.profile_image)
        preferences_complete = bool(preferences and all([
            preferences.travel_style,
            preferences.top_destination,
            preferences.travel_start_date,
            preferences.travel_end_date,
            preferences.budget_level
        ]))
        interests_exist = profile.traveler_interests.exists()  # type: ignore

        is_complete = profile_complete and preferences_complete and interests_exist

        return Response({"is_complete": is_complete})



class TravelChoicesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "travel_styles": [
                {"value": choice[0], "label": choice[1]}
                for choice in TravelerPreferences._meta.get_field("travel_style").choices # type: ignore
            ],
            "budget_levels": [
                {"value": choice[0], "label": choice[1]}
                for choice in TravelerPreferences._meta.get_field("budget_level").choices # type: ignore
            ]
        })
    
