from django.conf.urls import url, include
from rest_framework import routers
from rooms.views import RoomViewSet, ItemViewSet

room_router = routers.DefaultRouter()
room_router.register(r"rooms", RoomViewSet, base_name="room")

item_router = routers.DefaultRouter()
item_router.register(r"items", ItemViewSet, base_name="item")

urlpatterns = [
    url(r"^", include(room_router.urls), name='rooms'),
    url(r"^", include(item_router.urls), name="items"),
]
