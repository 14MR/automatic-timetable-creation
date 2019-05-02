from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from schedule.views import EventViewSet, GenerateViewSet, SchedulesViewSet

router = routers.DefaultRouter()
router.register("", SchedulesViewSet, basename="schedules")
router.register(r"events", EventViewSet, basename="event")
router.register(r"generate", GenerateViewSet, basename="generate")

urlpatterns = [url(r"^", include(router.urls), name="schedules")]
