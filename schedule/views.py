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
        events = Event.objects.filter(date__gte=start, date__lte=end)

        dates = events.values_list('date', flat=True)

        for date in dates:
                d_events = Event.objects.filter(date=date)
                resp[str(date)] = EventSerializer(d_events, many=True).data

        # all_timeslots = Timeslot.objects.none()
        # for day_choice in DaysOfWeek.choices:
        #     timeslots = Timeslot.objects.filter(day_of_week=day_choice[0], events__isnull=False)
        #     all_timeslots |= timeslots
        #     day_classes = []
        #     for timeslot in timeslots:
        #         classes = Event.objects.filter(timeslot=timeslot)
        #         # print("classes")
        #         # print(classes)
        #         timeslot_classes = []
        #         for my_class in classes:
        #             print("my class")
        #
        #             class_data = {
        #                 "class": my_class.current_class.course.title,
        #                 "type": str(my_class.current_class.type),
        #                 "teacher_name": my_class.current_class.teacher.first_name + ' ' + my_class.current_class.teacher.last_name,
        #                 "room": my_class.room.number,
        #             }
        #             timeslot_classes.append(class_data)
        #
        #         day_classes.append(timeslot_classes)
        #
        #     response[day_choice[1].lower()] = day_classes
        #
        # response['timeslots'] = list(set([f'{t.starting_time} - {t.ending_time}' for t in
        #                                   all_timeslots.only('starting_time', 'ending_time').distinct()]))

        # response = EventSerializer(events, many=True).data


        return Response(resp, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = EventSerializer(instance).data
        instance.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)
