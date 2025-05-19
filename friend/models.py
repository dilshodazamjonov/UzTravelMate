from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='user', verbose_name='Пользователь')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends', verbose_name='Друзья')

    def __str__(self): return self.user.username

    def add_friend(self, account):
        if account not in self.friends.all(): self.friends.add(account)

    def remove_friend(self, account):
        if account in self.friends.all(): self.friends.remove(account)

    def unfriend(self, removee):
        self.remove_friend(removee)
        FriendList.objects.get(user=removee).remove_friend(self.user)

    def is_mutual_friend(self, friend):
        return friend in self.friends.all()

    class Meta:
        verbose_name = 'Список друзей'
        verbose_name_plural = 'Списки друзей'
        ordering = ['user']

class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_requests",
                               verbose_name='Отправитель')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_requests",
                                 verbose_name='Получатель')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    def __str__(self): return f'Заявка от {self.sender.username} к {self.receiver.username}'

    def accept(self):
        receiver_friends_list, _ = FriendList.objects.get_or_create(user=self.receiver)
        sender_friends_list, _ = FriendList.objects.get_or_create(user=self.sender)
        receiver_friends_list.add_friend(self.sender)
        sender_friends_list.add_friend(self.receiver)
        self.is_active = False
        self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'Заявка в друзья'
        verbose_name_plural = 'Заявки в друзья'
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['sender', 'receiver'])]
        constraints = [models.UniqueConstraint(fields=['sender', 'receiver'], condition=models.Q(is_active=True),
                                               name='unique_active_friend_request')]
