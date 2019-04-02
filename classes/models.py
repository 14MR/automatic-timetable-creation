from django.core.validators import MaxValueValidator
from django.db import models

from classes.enums import SemesterType
from users.models import YearGroup, Group, User


class Semester(models.Model):
    year = models.PositiveSmallIntegerField()
    type = models.PositiveSmallIntegerField(verbose_name="type of semester", choices=SemesterType.choices)

    def __str__(self):
        return f"{self.get_type_display()} semester in {self.year} year"


class Course(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    year_group = models.ForeignKey(YearGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} course for {self.year_group} on {self.semester}"


class ClassType(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.ForeignKey(ClassType, on_delete=models.CASCADE)
    per_week = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10)])
    groups = models.ManyToManyField(Group)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __groups__(self):
        return ", ".join([group.__str__() for group in self.groups.all()])

    def __str__(self):
        return f"{self.type} on {self.course}"

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
