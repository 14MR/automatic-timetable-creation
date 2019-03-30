from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from schedule.views import EventViewSet

router = routers.DefaultRouter()
router.register(r"events", EventViewSet, basename="event")

urlpatterns = [
    url(r"^", include(router.urls), name="schedules"),
]
