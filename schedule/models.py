from django.core.validators import MaxValueValidator
from django.db import models
from rest_framework.compat import MinValueValidator

from classes.models import Semester, Class
from rooms.models import Room
from schedule.enums import DaysOfWeek


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


class Timeslot(models.Model):
    day_of_week = models.PositiveSmallIntegerField(validators=[MaxValueValidator(7), MinValueValidator(0)],
                                                   choices=DaysOfWeek.choices)
    starting_time = models.TimeField()
    ending_time = models.TimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(day_of_week__gte=0), name='day_of_week_gte_0'),
            models.CheckConstraint(check=models.Q(day_of_week__lte=7), name='day_of_week_lte_7'),
        ]
