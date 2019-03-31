"""PyTest tests for 'rooms' application """
from django.db.models import Max
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from rooms.models import RoomType, Room, ItemType, Item
from users.models import User

auditorium = {"name": "Auditoriums"}
room = {"number": 108, "capacity": 100, "is_yellow": False}

projector = {"name": "Projector"}

c_projector = {"name": "Cool Projector"}


class TestRooms(APITestCase):
    def setUp(self):
        self.auditorium = RoomType.objects.create(**auditorium)
        room["type_id"] = self.auditorium.id
        self.room = Room.objects.create(**room)
        self.projector = ItemType.objects.create(**projector)
        c_projector["type_id"] = self.projector.id
        c_projector["room_id"] = self.room.id
        self.c_projector = Item.objects.create(**c_projector)

        self.user = User.objects.create(email="test@test.com", is_active=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_room(self):
        rooms_count = Room.objects.count()
        url = reverse("room-list")
        data = {
            "number": 313,
            "capacity": 50,
            "is_yellow": True,
            "type_id": self.auditorium.id,
        }
        response_post = self.client.post(url, data, format="json")
        response_get = self.client.get(url)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 1 + rooms_count)

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), Room.objects.count())

    def test_view_rooms(self):
        url = reverse("room-list")
        response = self.client.get(url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), Room.objects.count())

    def test_view_one_room(self):
        url = reverse("room-detail", args=(self.room.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number"], self.room.number)

    def test_one_impossible_room(self):
        new_room = {
            "number": 110,
            "capacity": 100,
            "is_yellow": False,
            "type_id": self.auditorium.id,
        }
        impossible_room = Room.objects.all().aggregate(Max("id"))["id__max"] + 1

        url = reverse("room-detail", args=(impossible_room,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(url, new_room, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse("room-items", args=(impossible_room,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        new_item = {"name": "dull projector", "item_id": self.projector.id}
        response = self.client.post(url, new_item, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_put_on_room(self):
        url = reverse("room-detail", args=(self.room.id,))
        new_room = {
            "number": 110,
            "capacity": 100,
            "is_yellow": 10,
            "type_id": self.auditorium.id,
        }
        response = self.client.put(url, new_room, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_on_room(self):
        new_room = {
            "number": 110,
            "capacity": 100,
            "is_yellow": True,
            "type_id": self.auditorium.id,
        }
        new_room = Room.objects.create(**new_room)
        url = reverse("room-detail", args=(new_room.id,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_room_types_view(self):
        count = RoomType.objects.count()

        url = reverse("room-types")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)

    def test_item_view(self):
        count = Item.objects.count()
        url = reverse("item-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)

    def test_add_item(self):
        count = Item.objects.count()
        new_item = {"name": "UnCool Projector", "type_id": self.projector.id}
        url = reverse("item-list")

        response = self.client.post(url, new_item, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), count + 1)

    def test_get_item_types(self):
        count = ItemType.objects.count()

        url = reverse("item-types")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, len(response.data))

    def test_get_items_of_the_room(self):
        url = "/api/v1/rooms/{}/items/".format(self.room.id)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], self.c_projector.id)

    def test_set_items_of_the_room(self):
        count = self.c_projector.room.items.count()
        url = reverse("room-items", args=(self.room.id,))

        new_item = [{"name": "Projector WD40", "type_id": self.projector.id}]
        response = self.client.post(url, new_item, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_item = {"name": 12, "item_id": self.projector.id}
        response = self.client.post(url, new_item, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = reverse("room-items", args=(self.room.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count + 1)
