from schedule.models import Event, Schedule, Semester, Class, Room
from rest_framework import serializers


class ScheduleSerializer(serializers.ModelSerializer):
    semester_id = serializers.PrimaryKeyRelatedField(
        source="semester", queryset=Semester.objects.all()
    )

    class Meta:
        model = Schedule
        fields = ("id", "semester_id")


class EvenSerializer(serializers.ModelSerializer):
    class_id = serializers.PrimaryKeyRelatedField(
        source="current_class", queryset=Class.objects.all()
    )
    room_id = serializers.PrimaryKeyRelatedField(
        source="room", queryset=Room.objects.all()
    )

    class Meta:
        model = Event
        fields = ("id", "class_id", "room_id", "start_time", "end_time", "date")
