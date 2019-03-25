from django.db import models

from classes.enums import SemesterType


class Semester(models.Model):
    year = models.PositiveSmallIntegerField()
    type = models.PositiveSmallIntegerField(choices=SemesterType.choices)


class Courses(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
