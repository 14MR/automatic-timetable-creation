from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from schedule.serializers import Event, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)
    queryset = Event.objects.all()

    @action(detail=False, methods=["get"])
    def my(self, request, *args, **kwargs):
        data = {
            "monday": [
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "NotSucci",
                        "room": "108",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "118",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
            ],
            "tuesday": [
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "SWP", "type": "lecture", "room": "108"},
                ],
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "NotSucci",
                        "room": "111",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
            ],
            "wednesday": [
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "NotSucci",
                        "room": "111",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
            ],
            "thursday": [
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "NotSucci",
                        "room": "111",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
            ],
            "friday": [
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "NotSucci",
                        "room": "111",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
            ],
            "saturday": [
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "NotSucci",
                        "room": "111",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
            ],
            "sunday": [
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
                [
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "NotSucci",
                        "room": "111",
                    },
                    {
                        "class": "Discrete Maths",
                        "type": "lab",
                        "teacher_name": "Succi",
                        "room": "108",
                    },
                    {"class": "", "type": "", "room": ""},
                ],
            ],
            "timeslots": ["09:00-10:30", "10:35-12:05"],
            "groups": ["B18-02", "B18-03", "B18-04"],
        }

        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = EventSerializer(instance).data
        instance.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)
