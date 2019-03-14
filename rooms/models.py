from django.db import models


class RoomType(models.Model):
    name = models.CharField(max_length=30)


class Rooms(models.Model):
    number = models.IntegerField()
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    is_yellow = models.BooleanField(default=False)


class ItemType(models.Model):
    name = models.CharField(max_length=30)


class Item(models.Model):
    name = models.CharField(max_length=30)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
