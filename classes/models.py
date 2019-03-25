from django.core.validators import MaxValueValidator
from django.db import models

from classes.enums import SemesterType
from users.models import YearGroup, Group, User


class Semester(models.Model):
    year = models.PositiveSmallIntegerField()
    type = models.PositiveSmallIntegerField(choices=SemesterType.choices)


class Course(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    year_group = models.ForeignKey(YearGroup, on_delete=models.CASCADE)


class ClassType(models.Model):
    title = models.CharField(max_length=20)


class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.ForeignKey(ClassType, on_delete=models.CASCADE)
    per_week = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    groups = models.ManyToManyField(Group)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

