import factory
import random

from classes.models import Semester, Course, Class, ClassType
from users.factory import YearGroupFactory, UserFactory


class SemesterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Semester

    year = random.randint(2018, 2100)
    type = random.choice([0, 1, 2])


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course

    title = factory.Faker("word")
    description = factory.Faker("sentence")
    semester = factory.SubFactory(SemesterFactory)
    year_group = factory.SubFactory(YearGroupFactory)


class ClassTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClassType

    title = random.choice(["Lecture", "Tutorial", "Lab"])


class ClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Class

    course = factory.SubFactory(CourseFactory)
    type = factory.SubFactory(ClassTypeFactory)
    per_week = random.randint(1, 10)
    teacher = factory.SubFactory(UserFactory)
