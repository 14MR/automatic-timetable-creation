from schedule.models import Event, Schedule, Semester, Class, Room, Timeslot
from rest_framework import serializers

from users.models import Group


class ScheduleSerializer(serializers.ModelSerializer):
    semester_id = serializers.PrimaryKeyRelatedField(
        source="semester", queryset=Semester.objects.all()
    )

    class Meta:
        model = Schedule
        fields = ("id", "semester_id")


class EventSerializer(serializers.ModelSerializer):
    group_id = serializers.PrimaryKeyRelatedField(source='group', queryset=Group.objects.all())
    timeslot_id = serializers.PrimaryKeyRelatedField(source='timeslot', queryset=Timeslot.objects.all())
    class_id = serializers.PrimaryKeyRelatedField(
        source="current_class", queryset=Class.objects.all()
    )
    room_id = serializers.PrimaryKeyRelatedField(
        source="room", queryset=Room.objects.all()
    )
    schedule_id = serializers.PrimaryKeyRelatedField(source='schedule', queryset=Schedule.objects.all())

    class Meta:
        model = Event
        fields = ("id", "class_id", "room_id", "group_id", "timeslot_id", "schedule_id", "date")
