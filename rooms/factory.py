import factory
import random

from factory import fuzzy

from rooms.models import ItemType
from rooms.models import Item
from rooms.models import RoomType
from rooms.models import Room


class RoomTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RoomType

    name = random.choice(["Lecture hall", "Auditorium"])


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    number = fuzzy.FuzzyInteger(100, 600)
    type = factory.SubFactory(RoomTypeFactory)
    capacity = fuzzy.FuzzyInteger(30, 60)
    is_yellow = fuzzy.FuzzyInteger(0, 1)


class ItemTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ItemType

    name = random.choice(
        [
            "Projector",
            "Whiteboard",
            "Blackboard",
            "Interactive board",
            "Window",
            "Bottled water",
            "Trashcan",
            "Sink",
            "Wi-Fi",
        ]
    )


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Faker("word")
    type = factory.SubFactory(ItemTypeFactory)
    room = factory.SubFactory(RoomFactory)
