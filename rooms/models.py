from django.db import models


class ItemType(models.Model):
    name = models.CharField(max_length=30)


class Item(models.Model):
    name = models.CharField(max_length=30)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)


class RoomType(models.Model):
    name = models.CharField(max_length=30)


class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField()
    is_yellow = models.BooleanField(default=False)
    items = models.ManyToManyField(Item, blank=True)
