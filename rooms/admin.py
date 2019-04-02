from django.contrib import admin
from rooms.models import Item, ItemType, Room, RoomType


class AdminItem(admin.ModelAdmin):
    list_display = ('name', 'type', 'room')


class AdminRoom(admin.ModelAdmin):
    list_display = ('number', 'type', 'capacity', 'is_yellow')
    list_filter = ('type', 'is_yellow')


admin.site.register(Item, AdminItem)
admin.site.register(ItemType)
admin.site.register(Room, AdminRoom)
admin.site.register(RoomType)
