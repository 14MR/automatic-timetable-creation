from django.db import models


class ItemType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=30)
    type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
    room = models.ForeignKey(
        "Room", on_delete=models.CASCADE, blank=True, null=True, related_name="items"
    )

    def __str__(self):
        return f"{self.type} {self.name} in room {self.room}"


class RoomType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class Room(models.Model):
    number = models.PositiveSmallIntegerField()
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField()
    is_yellow = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} {self.number} with capacity {self.capacity}. " \
            f"{'Yellow' if self.is_yellow else 'Not yellow'}"
