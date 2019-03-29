from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from schedule.serializers import ScheduleSerializer, Schedule, Event, EvenSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]
    queryset = Schedule.objects.all()


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EvenSerializer
    permission_classes = [AllowAny]
    queryset = Event.objects.all()
