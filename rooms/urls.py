from django.conf.urls import url, include
from rest_framework import routers
from rooms.views import RoomViewSet, ItemViewSet

router = routers.DefaultRouter()
router.register(r"items", ItemViewSet, base_name="item")
router.register(r"", RoomViewSet, base_name="room")

urlpatterns = [
    url(r"^", include(router.urls), name="items"),
]
