# Create your tests here.
from django.db.models import Max
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from schedule.factory import EventFactory
from schedule.models import Event


class TestEvents(APITestCase):
    def setUp(self):
        self.event = EventFactory.create_batch(size=1)[0]

    def test_view_event(self):
        # Tests GET(200) on /schedules/events/
        event_count = Event.objects.count()
        url = reverse("event-list")
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data['results']), event_count)

    def test_create_event(self):
        # Tests POST (201) on /schedules/events/
        event_count = Event.objects.count()
        new_event_data = {
            "start_time": "09:00:00",
            "end_time": "10:30:00",
            "class_id": self.event.current_class_id,
            "date": "2017-07-21",
            "room_id": self.event.room_id,
        }
        url = reverse("event-list")

        response_post = self.client.post(url, new_event_data, format="json")
        response_get = self.client.get(url)

        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(event_count + 1, Event.objects.count())
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data['results']), Event.objects.count())

    def test_delete_event(self):
        # Tests DELETE (200) on /schedules/events/{id}/
        event_count = Event.objects.count()
        event = EventFactory.create_batch(size=1)[0]
        url = reverse("event-detail", args=(event.id,))
        response_delete = self.client.delete(url)

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete.data["id"], event.id)
        self.assertEqual(event_count, Event.objects.count())

    def test_put_event(self):
        # Test PUT(200) on /schedules/events/{id}/
        new_event_data = {
            "start_time": self.event.start_time,
            "end_time": self.event.end_time,
            "class_id": self.event.current_class_id,
            "date": "2017-07-23",
            "room_id": self.event.room_id,
        }
        url = reverse("event-detail", args=(self.event.id,))
        response = self.client.put(url, new_event_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["date"], new_event_data["date"])
        self.assertEqual(
            str(Event.objects.get(pk=self.event.id).date), new_event_data["date"]
        )

    def test_view_single_event(self):
        # Tests GET(200) on /schedules/events/{id}/
        url = reverse("event-detail", args=(self.event.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["room_id"], self.event.room_id)

    def test_erroneous_get_event(self):
        # Tests GET(404) on /schedules/events/{id}/
        max_id = Event.objects.all().aggregate(Max("id"))["id__max"] + 1

        url = reverse("event-detail", args=(max_id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_post_event(self):
        # Tests POST(400) on /schedules/events/
        event_count = Event.objects.count()
        url = reverse("event-list")
        new_event_data = {
            "start_time": "25:00:00",
            "end_time": "26:30:00",
            "class_id": self.event.current_class_id,
            "date": "2017-07-21",
            "room_id": self.event.room_id,
        }
        response_post = self.client.post(url, new_event_data, format="json")
        self.assertEqual(response_post.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(event_count, Event.objects.count())

    def test_erroneous_put_event(self):
        # Tests PUT(400,404) on /schedules/events/{id}/
        new_event_data = {"date": "1000-23-23"}

        url = reverse("event-detail", args=(self.event.id,))
        response_put = self.client.put(url, new_event_data, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_400_BAD_REQUEST)

        max_id = Event.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("event-detail", args=(max_id,))
        response_put = self.client.put(url, new_event_data, format="json")

        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_delete_event(self):
        # Tests DELETE(404) on /schedules/events/{id}/
        max_id = Event.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("event-detail", args=(max_id,))

        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)
