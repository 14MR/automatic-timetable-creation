from django.contrib import admin
from rooms.models import Item, ItemType, Room, RoomType

admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(Room)
admin.site.register(RoomType)
