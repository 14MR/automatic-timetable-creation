import datetime
import random

import factory

from factory.fuzzy import FuzzyDate

from classes.factory import SemesterFactory, ClassFactory
from rooms.factory import RoomFactory
from schedule.models import Schedule, Event, Timeslot
from users.factory import GroupFactory


class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schedule

    semester = factory.SubFactory(SemesterFactory)


class TimeslotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Timeslot
        django_get_or_create = ('id', 'starting_time', 'ending_time', 'day_of_week')

    id = 1
    starting_time = "09:00:00"
    ending_time = "10:30:00"
    day_of_week = 0


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    timeslot = factory.SubFactory(TimeslotFactory)
    schedule = factory.SubFactory(ScheduleFactory)
    group = factory.SubFactory(GroupFactory)
    current_class = factory.SubFactory(ClassFactory)
    date = FuzzyDate(datetime.datetime(2018, 1, 1), datetime.datetime(2100, 1, 1))
    room = factory.SubFactory(RoomFactory)

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        hour_ = random.randint(9, 20)
        minute_ = 5 * random.randint(1, 11)
        obj.start_time = datetime.time(hour=hour_, minute=minute_)
        new_minute_ = minute_ + 30
        if new_minute_ > 59:
            hour_ += 1
            new_minute_ -= 60
        obj.end_time = datetime.time(hour=hour_ + 1, minute=new_minute_)
