from django.contrib import admin
from .models import FriendList, FriendRequest


@admin.register(FriendList)
class FriendListAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_friends')
    search_fields = ('user__username', 'friends__username')
    filter_horizontal = ('friends',)

    def get_friends(self, obj):
        return ", ".join([friend.username for friend in obj.friends.all()])
    get_friends.short_description = 'Друзья'


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sender', 'receiver', 'is_active', 'timestamp')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('is_active', 'timestamp')
    readonly_fields = ('timestamp',)

    def has_add_permission(self, request):
        return False  # disable manual creation

    def has_change_permission(self, request, obj=None):
        return False  # disable manual editing
