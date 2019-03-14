from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from rooms.views import RoomViewSet

router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    url(r'^', include(router.urls)),
]
