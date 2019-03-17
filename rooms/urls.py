from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from rooms.views import RoomViewSet, ItemViewSet

room_router = routers.DefaultRouter()
room_router.register(r'rooms', RoomViewSet, basename='room')

item_router = routers.DefaultRouter()
item_router.register(r'items', ItemViewSet, basename='item')
urlpatterns = [
    url(r'^', include(room_router.urls)),
    url(r'^', include(item_router.urls))