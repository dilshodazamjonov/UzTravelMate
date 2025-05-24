# views.py
from django.views.decorators.http import require_GET
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status

from account.serializers import AccountSerializer

from .auth import CsrfExemptSessionAuthentication
from .serializers import *

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def send_friend_request_view(request):
    serializer = FriendRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        friend_request = serializer.save()
        return Response(
            {'message': 'Запрос в друзья успешно отправлен.', 'friend_request_id': friend_request.id},
            status=status.HTTP_201_CREATED
        )
    return Response({'ошибки': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_requests_view(request):
    user = request.user
    friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
    serializer = FriendRequestListSerializer(friend_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friends_list_view(request):
    user = request.user

    try:
        friend_list = FriendList.objects.get(user=user)
    except FriendList.DoesNotExist:
        return Response({'error': f'Список друзей пользователя {user.username} не найден.'},
                        status=status.HTTP_404_NOT_FOUND)

    friends = friend_list.friends.all()
    serializer = FriendSerializer(friends, many=True, context={'request': request})
    return Response({'friends': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def accept_friend_request_view(request):
    serializer = AcceptFriendRequestSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def remove_friend_view(request):
    serializer = RemoveFriendSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def decline_friend_request_view(request):
    serializer = DeclineFriendRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cancel_friend_request_view(request):
    serializer = CancelFriendRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        result = serializer.save()
        return Response(result, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def search_users(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return Response([])

    users = Account.objects.filter(
        Q(username__icontains=query) |
        Q(email__icontains=query)
    )

    serializer = AccountSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)



