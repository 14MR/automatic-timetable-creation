"""PyTest tests for 'rooms' application """
from django.db.models import Max
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rooms.models import RoomType, Room, ItemType, Item
from rooms.serializers import RoomSerializer

auditorium = {
    'name': 'Auditoriums'
}
room = {
    "number": 108,
    "capacity": 100,
    "is_yellow": False
}

projector = {
    "name": "Projector"
}

c_projector = {
    "name": "Cool Projector"
}


class TestRooms(APITestCase):
    def setUp(self):
        self.auditorium = RoomType.objects.create(**auditorium)
        room['type_id'] = self.auditorium.id
        self.room = Room.objects.create(**room)
        self.projector = ItemType.objects.create(**projector)
        c_projector['type_id'] = self.projector.id
        c_projector['room_id'] = self.room.id
        self.c_projector = Item.objects.create(**c_projector)

    def test_create_room(self):
        rooms_count = Room.objects.count()
        url = "/api/v1/rooms/"
        data = {"number": 313, "capacity": 50, "is_yellow": True, 'type_id': self.auditorium.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 1 + rooms_count)

    def test_view_rooms(self):
        url = "/api/v1/rooms/"
        response = self.client.get(url, {}, format='json')
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), Room.objects.count())

    def test_view_one_room(self):
        url = "/api/v1/rooms/{}/".format(self.room.id)
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], self.room.number)

    def test_one_impossible_room(self):
        new_room = {"number": 110, "capacity": 100, "is_yellow": False, 'type_id': self.auditorium.id}
        impossible_room = Room.objects.all().aggregate(Max('id'))['id__max'] + 1

        url = "/api/v1/rooms/{}/".format(impossible_room)
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(url, new_room, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = "/api/v1/rooms/{}/items/".format(impossible_room)

        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        new_item = {"name": "dull projector", "item_id": self.projector.id}
        response = self.client.post(url, new_item, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_put_on_room(self):
        url = "/api/v1/rooms/{}/".format(self.room.id)
        new_room = {"number": 110, "capacity": 100, "is_yellow": 10, 'type_id': self.auditorium.id}
        response = self.client.put(url, new_room, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_on_room(self):
        new_room = {"number": 110, "capacity": 100, "is_yellow": True, 'type_id': self.auditorium.id}
        new_room = Room.objects.create(**new_room)
        url = "/api/v1/rooms/{}/".format(new_room.id)

        response = self.client.delete(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_room_types_view(self):
        count = RoomType.objects.count()

        url = "/api/v1/rooms/types/"

        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)

    def test_item_view(self):
        count = Item.objects.count()
        url = "/api/v1/items/"

        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count)

    def test_add_item(self):
        count = Item.objects.count()
        new_item = {"name": "UnCool Projector", 'type_id': self.projector.id}
        url = "/api/v1/items/"

        response = self.client.post(url, new_item, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), count + 1)

    def test_get_item_types(self):
        count = ItemType.objects.count()

        url = "/api/v1/items/types/"

        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(count, len(response.data))

    def test_get_items_of_the_room(self):
        url = "/api/v1/rooms/{}/items/".format(self.room.id)

        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.c_projector.id)

    def test_set_items_of_the_room(self):
        count = self.c_projector.room.items.count()
        url = "/api/v1/rooms/{}/items/".format(self.room.id)

        new_item = [
            {
                "name": "Projector WD40",
                "type_id": self.projector.id
            }
        ]
        response = self.client.post(url, new_item, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_item = {"name": 12, "item_id": self.projector.id}
        response = self.client.post(url, new_item, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        url = "/api/v1/rooms/{}/items/".format(self.room.id)

        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), count + 1)