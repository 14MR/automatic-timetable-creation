from django.db import models
from classes.models import Semester, Class
from rooms.models import Room


class Schedule(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.semester} schedule"


class Event(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    current_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
