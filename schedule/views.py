from celery.result import AsyncResult
from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, status, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from atc.celery import app
from schedule.models import Schedule
from schedule.serializers import Event, EventSerializer
from schedule.tasks import generate_table_and_save
from users.enums import RoleType
from users.permissions import IsDOEOrHigher


class EventViewSet(viewsets.ViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    @action(detail=False, methods=["get"])
    def my(self, request, *args, **kwargs):
        resp = {}

        today = timezone.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        events = Event.objects.filter(date__gte=start, date__lte=end)

        if request.user.role == RoleType.student:  # students see only their events
            events = events.filter(group__user=request.user)

        dates = events.values_list('date', flat=True).distinct()

        for date in dates:
            d_events = events.filter(date=date)
            resp[str(date)] = EventSerializer(d_events, many=True).data

        return Response(resp, status=status.HTTP_200_OK)


class SchedulesViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = EventSerializer
    queryset = Schedule.objects.all()

    def retrieve(self, request, pk=None):
        schedule = self.get_object()
        resp = {}

        today = timezone.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        events = Event.objects.filter(date__gte=start, date__lte=end, schedule=schedule)
        dates = events.values_list('date', flat=True).distinct()

        for date in dates:
            d_events = events.filter(date=date)
            resp[str(date)] = EventSerializer(d_events, many=True).data

        return Response(resp, status=status.HTTP_200_OK)


class GenerateViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsDOEOrHigher)

    def list(self, request, *args, **kwargs):
        uid = request.query_params.get('uid', False)

        if not uid:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        res = AsyncResult(uid, app=app)

        return Response({"ready": res.successful()})

    def create(self, request, *args, **kwargs):
        uid = generate_table_and_save.delay()

        return Response({"uid": uid.id})
