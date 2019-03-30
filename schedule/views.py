from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from schedule.serializers import Event, EvenSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EvenSerializer
    permission_classes = [AllowAny]
    queryset = Event.objects.all()
