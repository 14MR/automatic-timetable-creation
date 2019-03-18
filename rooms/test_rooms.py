"""PyTest tests for 'rooms' application """

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rooms.models import RoomType, Room
from rooms.serializers import RoomSerializer

auditorium = {
    'name': 'Auditoriums'
}
room = {
    "number": 108,
    "type_id": 1,
    "capacity": 100,
    "is_yellow": False
}


class TestRooms(APITestCase):
    def setUp(self):
        self.auditorium = RoomType.objects.create(**auditorium)
        self.room = Room.objects.create(**room)

    def test_create_room(self):
        rooms_count = Room.objects.count()
        url = reverse('rooms-rooms')
        data = {
            "number": 313,
            "type_id": 1,
            "capacity": 50,
            "is_yellow": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), 1 + rooms_count)

    # def test_view_rooms(self):
    #     url = reverse('rooms-rooms')
    #     response = self.client.get(url, {}, format='json')
    #     print(response)
    #     self.assertEqual(True)
