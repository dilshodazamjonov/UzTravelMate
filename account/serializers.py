from friend.utils import get_friend_request_or_false
from .models import *
from rest_framework import serializers
from friend.models import FriendList, FriendRequest
from friend.friend_request_status import FriendRequestStatus


class AccountSerializer(serializers.ModelSerializer):
    is_self = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    request_sent = serializers.SerializerMethodField()
    pending_friend_request_id = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'id', 'email', 'username', 'profile_image', 'hide_email',
            'is_self', 'is_friend', 'request_sent', 'pending_friend_request_id', 'friends'
        ]

    def get_is_self(self, obj):
        request = self.context.get('request')
        return request.user == obj if request else False

    def get_is_friend(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                friend_list = FriendList.objects.get(user=obj)
                return request.user in friend_list.friends.all()
            except FriendList.DoesNotExist:
                return False
        return False

    def get_request_sent(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated or request.user == obj:
            return FriendRequestStatus.NO_REQUEST_SENT.value

        if get_friend_request_or_false(sender=obj, receiver=request.user):
            return FriendRequestStatus.THEM_SENT_TO_YOU.value
        elif get_friend_request_or_false(sender=request.user, receiver=obj):
            return FriendRequestStatus.YOU_SENT_TO_THEM.value
        return FriendRequestStatus.NO_REQUEST_SENT.value

    def get_pending_friend_request_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            friend_request = get_friend_request_or_false(sender=obj, receiver=request.user)
            if friend_request:
                return friend_request.id
        return None

    def get_friends(self, obj):
        try:
            friend_list = FriendList.objects.get(user=obj)
            return [{'id': friend.id, 'username': friend.username} for friend in friend_list.friends.all()]
        except FriendList.DoesNotExist:
            return []



class TravelerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelerProfile
        fields = [
            'profile_image',
            'date_of_birth',
            'interests',
            'travel_style',
            'top_destination',
        ]
        extra_kwargs = {
            'profile_image': {'required': False},
            'date_of_birth': {'required': False},
            'interests': {'required': False},
            'travel_style': {'required': False},
            'top_destination': {'required': False},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ['latitude', 'longitude', 'updated_at']
        read_only_fields = ['updated_at']




