from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from schedule.views import ScheduleViewSet, EvenViewSet

schedule_router = routers.DefaultRouter()
schedule_router.register(r"schedules", ScheduleViewSet, basename="schedule")

event_router = routers.DefaultRouter()
event_router.register(r"events", EvenViewSet, basename="event")

urlpatterns = [
    url(r"^", include(schedule_router.urls), name="schedules"),
    url(r"^", include(event_router.urls), name="events"),
]
