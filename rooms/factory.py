import factory
import random

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

    number = random.randint(100, 600)
    type = factory.SubFactory(RoomTypeFactory)
    capacity = 10 * random.randint(3, 20)
    is_yellow = number > 299 if random.choice([True, False]) else False


class ItemTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ItemType

    name = random.choice(["Projector", "Whiteboard", "Blackboard",
                          "Interactive board", "Window", "Bottled water",
                          "Trashcan", "Sink", "Wi-Fi"])


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = factory.Faker("word")
    type = factory.SubFactory(ItemTypeFactory)
    room = factory.SubFactory(RoomFactory)
