# serializers.py
from rest_framework import serializers
from account.models import Account
from friend.models import FriendRequest


class FriendRequestSerializer(serializers.Serializer):
    receiver_username = serializers.CharField()

    def validate_receiver_username(self, value):
        try:
            receiver = Account.objects.get(username=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким именем не найден.")

        if self.context['request'].user == receiver:
            raise serializers.ValidationError("Вы не можете отправить запрос в друзья самому себе.")

        return value

    def create(self, validated_data):
        sender = self.context['request'].user
        receiver = Account.objects.get(username=validated_data['receiver_username'])

        friend_requests = FriendRequest.objects.filter(sender=sender, receiver=receiver)

        for req in friend_requests:
            if req.is_active:
                raise serializers.ValidationError(
                    "Вы уже отправили этому пользователю запрос в друзья. Пожалуйста, дождитесь ответа.")

        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        return friend_request
