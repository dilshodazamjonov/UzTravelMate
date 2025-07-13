from friend.utils import get_friend_request_or_false
from .models import Account, TravelerProfile, UserLocation
from friend.models import FriendList
from rest_framework import serializers
from friend.friend_request_status import FriendRequestStatus
from user_preferences.serializers import TravelerPreferencesSerializer
from user_preferences.models import Interest, TravelerInterest
from user_preferences.models import TravelerPreferences


class AccountSerializer(serializers.ModelSerializer):
    is_self = serializers.SerializerMethodField()
    is_friend = serializers.SerializerMethodField()
    request_sent = serializers.SerializerMethodField()
    pending_friend_request_id = serializers.SerializerMethodField()
    friends = serializers.SerializerMethodField()

    class Meta:
        model = Account  # noqa: F405
        fields = [
            'id', 'email', 'username', 'profile_image', 'private',
            'is_self', 'is_friend', 'request_sent', 'pending_friend_request_id',
            'friends'
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
                return friend_request.pk
        return None

    def get_friends(self, obj):
        try:
            friend_list = FriendList.objects.get(user=obj)
            return [{'id': friend.id, 'username': friend.username} for friend in friend_list.friends.all()]
        except FriendList.DoesNotExist:
            return []


class TravelerProfileSerializer(serializers.ModelSerializer):
    preferences = TravelerPreferencesSerializer(required=False)
    interests = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all()),
        required=False
    )

    class Meta:
        model = TravelerProfile
        fields = [
            'profile_image',
            'date_of_birth',
            'preferences',
            'interests',
        ]
        extra_kwargs = {
            'profile_image': {'required': False},
            'date_of_birth': {'required': False},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Add preferences data
        preferences_instance = getattr(instance, 'preferences', None)
        data['preferences'] = TravelerPreferencesSerializer(preferences_instance).data if preferences_instance else None

        # Add interest IDs
        interests = TravelerInterest.objects.filter(traveler=instance).values_list('interest__id', flat=True)
        data['interests'] = list(interests)

        return data

    def update(self, instance, validated_data):
        # Update base profile fields
        profile_fields = ['profile_image', 'date_of_birth']
        for field in profile_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()

        # Handle preferences update or creation
        preferences_data = validated_data.get('preferences')
        if preferences_data:
            preferences_instance, _ = TravelerPreferences.objects.get_or_create(traveler=instance)
            for attr, value in preferences_data.items():
                setattr(preferences_instance, attr, value)
            preferences_instance.save()

        # Handle interests
        interests_data = validated_data.get('interests')
        if interests_data is not None:
            TravelerInterest.objects.filter(traveler=instance).delete()
            TravelerInterest.objects.bulk_create([
                TravelerInterest(traveler=instance, interest=interest) for interest in interests_data
            ])

        return instance



class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ['latitude', 'longitude', 'updated_at']
        read_only_fields = ['updated_at']




