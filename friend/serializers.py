from rest_framework import serializers
from core_account.models import Account
from friend.models import FriendRequest, FriendList

class FriendRequestSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()

    def validate_receiver_id(self, value):
        request_user = self.context['request'].user
        try:
            receiver = Account.objects.get(pk=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким ID не найден.")

        if request_user == receiver:
            raise serializers.ValidationError("Вы не можете отправить запрос в друзья самому себе.")

        self.receiver = receiver  # Save for use in create()
        return value

    def create(self, validated_data):
        sender = self.context['request'].user
        receiver = self.receiver  # set in validate_receiver_id()

        # Check if already friends
        try:
            sender_friend_list = FriendList.objects.get(user=sender)
            if sender_friend_list.is_mutual_friend(receiver):
                raise serializers.ValidationError("Вы уже находитесь в списке друзей с этим пользователем.")
        except FriendList.DoesNotExist:
            pass

        # Check if an active friend request already exists
        friend_requests = FriendRequest.objects.filter(sender=sender, receiver=receiver)
        for req in friend_requests:
            if req.is_active:
                raise serializers.ValidationError(
                    "Вы уже отправили этому пользователю запрос в друзья. Пожалуйста, дождитесь ответа.")

        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        return friend_request


class FriendSerializer(serializers.ModelSerializer):
    is_mutual_friend = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'is_mutual_friend']

    def get_is_mutual_friend(self, obj):
        request_user = self.context['request'].user
        auth_user_friend_list = FriendList.objects.get(user=request_user)
        return auth_user_friend_list.is_mutual_friend(obj)



class FriendRequestListSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'sender_username', 'timestamp']


# "friend_request_id": 3
class AcceptFriendRequestSerializer(serializers.Serializer):
    friend_request_id = serializers.IntegerField()

    def validate_friend_request_id(self, value):
        try:
            friend_request = FriendRequest.objects.get(pk=value)
        except FriendRequest.DoesNotExist:
            raise serializers.ValidationError("Friend request not found.")
        self.friend_request = friend_request
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        friend_request = self.friend_request

        if friend_request.receiver != user:
            raise serializers.ValidationError("That is not your request to accept.")

        friend_request.accept()
        return {"response": "Friend request accepted."}

# "receiver_user_id": id
class RemoveFriendSerializer(serializers.Serializer):
    receiver_user_id = serializers.IntegerField()

    def validate_receiver_user_id(self, value):
        request_user = self.context['request'].user

        if request_user.id == value:
            raise serializers.ValidationError("Вы не можете удалить самого себя из друзей.")

        try:
            self.removee = Account.objects.get(pk=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Пользователь, которого вы пытаетесь удалить, не существует.")

        # Проверка, есть ли пользователь в списке друзей
        friend_list = FriendList.objects.get(user=request_user)
        if not friend_list.is_mutual_friend(self.removee):
            raise serializers.ValidationError("Этот пользователь не находится в вашем списке друзей.")

        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        friend_list = FriendList.objects.get(user=user)
        friend_list.unfriend(self.removee)
        return {"response": "Пользователь успешно удалён из друзей."}

# "friend_request_id" : id
class DeclineFriendRequestSerializer(serializers.Serializer):
    friend_request_id = serializers.IntegerField()

    def validate_friend_request_id(self, value):
        user = self.context['request'].user
        try:
            self.friend_request = FriendRequest.objects.get(pk=value)
        except FriendRequest.DoesNotExist:
            raise serializers.ValidationError("Запрос на добавление в друзья не найден.")

        if self.friend_request.receiver != user:
            raise serializers.ValidationError("Это не ваш запрос на добавление в друзья.")

        return value

    def save(self, **kwargs):
        self.friend_request.decline()
        return {"response": "Запрос на добавление в друзья отклонён."}



# "receiver_user_id" : id
class CancelFriendRequestSerializer(serializers.Serializer):
    receiver_user_id = serializers.IntegerField()

    def validate_receiver_user_id(self, value):
        try:
            self.receiver = Account.objects.get(pk=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")
        return value

    def save(self, **kwargs):
        sender = self.context['request'].user
        receiver = self.receiver

        friend_requests = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True)
        if not friend_requests.exists():
            raise serializers.ValidationError("Нет активного запроса в друзья, который можно отменить.")

        for req in friend_requests:
            req.cancel()

        return {"response": "Запрос в друзья был успешно отменён."}

