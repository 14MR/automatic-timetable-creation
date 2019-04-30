from classes.serializers import ClassSerializer
from rooms.serializers import RoomSerializer
from schedule.models import Event, Schedule, Semester, Class, Room, Timeslot
from rest_framework import serializers

from users.models import Group
from users.serializers import GroupSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    semester_id = serializers.PrimaryKeyRelatedField(
        source="semester", queryset=Semester.objects.all()
    )

    class Meta:
        model = Schedule
        fields = ("id", "semester_id")


class EventSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=True)
    starting_time = serializers.DateTimeField(source='timeslot.starting_time')
    ending_time = serializers.DateTimeField(source='timeslot.ending_time')
    # class_id = serializers.PrimaryKeyRelatedField(
    #     source="current_class", queryset=Class.objects.all()
    # )
    class_info = ClassSerializer(source='current_class')
    room = RoomSerializer()

    class Meta:
        model = Event
        fields = ("id", "class_info", "room", "group", "starting_time", "ending_time", "date")
