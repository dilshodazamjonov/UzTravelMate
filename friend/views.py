from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from core_account.serializers import AccountSerializer
from core_account.models import Account
from .models import FriendRequest, FriendList

from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    FriendRequestSerializer,
    FriendRequestListSerializer,
    AcceptFriendRequestSerializer,
    RemoveFriendSerializer,
    DeclineFriendRequestSerializer,
    CancelFriendRequestSerializer,
    FriendSerializer
)

class FriendRequestReceivedListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список входящих запросов в друзья"
    )
    def get(self, request):
        friend_requests = FriendRequest.objects.filter(receiver=request.user, is_active=True)
        serializer = FriendRequestListSerializer(friend_requests, many=True)
        return Response(serializer.data)


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=FriendRequestSerializer)
    def post(self, request):
        serializer = FriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            friend_request = serializer.save()
            return Response(
                {'message': 'Запрос в друзья успешно отправлен.', 'friend_request_id': friend_request.id},
                status=status.HTTP_201_CREATED
            )
        return Response({'ошибки': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class IncomingFriendRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Получить список входящих запросов в друзья")
    def get(self, request):
        friend_requests = FriendRequest.objects.filter(receiver=request.user, is_active=True)
        serializer = FriendRequestListSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FriendsListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Получить список друзей")
    def get(self, request):
        user = request.user
        try:
            friend_list = FriendList.objects.get(user=user)
        except FriendList.DoesNotExist:
            return Response({'error': f'Список друзей пользователя {user.username} не найден.'},
                            status=status.HTTP_404_NOT_FOUND)

        friends = friend_list.friends.all()
        serializer = FriendSerializer(friends, many=True, context={'request': request})
        return Response({'friends': serializer.data}, status=status.HTTP_200_OK)


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AcceptFriendRequestSerializer)
    def post(self, request):
        serializer = AcceptFriendRequestSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RemoveFriendSerializer)
    def post(self, request):
        serializer = RemoveFriendSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeclineFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=DeclineFriendRequestSerializer)
    def post(self, request):
        serializer = DeclineFriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CancelFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CancelFriendRequestSerializer)
    def post(self, request):
        serializer = CancelFriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchUsersView(APIView):
    @swagger_auto_schema(operation_description="Поиск пользователей по username или email (минимум 2 символа)")
    def get(self, request):
        query = request.GET.get('q', '')
        if len(query) < 2:
            return Response([])

        users = Account.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

        serializer = AccountSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
