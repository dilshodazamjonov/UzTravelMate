from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import GoogleOneTapSerializer, RegisterSerializer, VerifyCodeSerializer
from drf_yasg.utils import swagger_auto_schema



User = get_user_model()


# core_account/serializers.py

User = get_user_model()

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]  # Allow any user to register

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Код подтверждения отправлен на указанный email"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny] 

    @swagger_auto_schema(request_body=VerifyCodeSerializer)
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.save()
            return Response({
                "message": "Email успешно подтвержден!",
                **tokens # type: ignore
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleOneTapLoginAPIView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    @swagger_auto_schema(request_body=GoogleOneTapSerializer)
    def post(self, request):
        serializer = GoogleOneTapSerializer(data=request.data)
        if serializer.is_valid():
            tokens = serializer.save()
            return Response({
                "status": "ok",
                **tokens # type: ignore
            })
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)