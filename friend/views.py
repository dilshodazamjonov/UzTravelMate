# views.py
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .auth import CsrfExemptSessionAuthentication
from .serializers import FriendRequestSerializer

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def send_friend_request_view(request):
    serializer = FriendRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        friend_request = serializer.save()
        return Response({'message': 'Запрос в друзья успешно отправлен.', 'friend_request_id': friend_request.id}, status=status.HTTP_201_CREATED)
    return Response({'ошибки': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





