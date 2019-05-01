from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from schedule.enums import DaysOfWeek
from schedule.models import Timeslot
from schedule.serializers import Event, EventSerializer
from datetime import datetime, timedelta


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)
    queryset = Event.objects.all()

    @action(detail=False, methods=["get"])
    def my(self, request, *args, **kwargs):
        resp = {}

        today = timezone.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        # events = Event.objects.filter(date__gte=start, date__lte=end)
        events = Event.objects.all()
        dates = events.values_list('date', flat=True)

        for date in dates:
            d_events = Event.objects.filter(date=date)
            resp[str(date)] = EventSerializer(d_events, many=True).data

        return Response(resp, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = EventSerializer(instance).data
        instance.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)
