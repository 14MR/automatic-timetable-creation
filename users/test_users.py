"""PyTest tests for 'users' application """

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, YearGroup, Group

user_data = {
    "first_name": "Bob",
    "last_name": "Bobov",
    "email": "bob_valid_email@kek.ru",
    "password": "12345678",
}


class TestAuth(APITestCase):
    def setUp(self):
        self.user = User.objects.create(**user_data)
        self.user.set_password(user_data["password"])
        self.user.save()

    def test_create_account(self):
        count = User.objects.count()
        url = reverse("users-signup")
        data = {
            "first_name": "first",
            "last_name": "name",
            "email": "valid_email@kek.ru",
            "password": "12345678",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1 + count)
        self.assertEqual(
            User.objects.get(email=data["email"]).first_name, data["first_name"]
        )

    def test_get_token(self):
        url = reverse("users-login")
        data = {"email": user_data.pop("email"), "password": user_data.pop("password")}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


group_data = {
    "number": 3,
}

year_group_data = {
    "year": 2017,
    "type": 1
}


class TestGroups(APITestCase):
    def setUp(self):
        self.year_group = YearGroup.objects.create(**year_group_data)
        group_data["year_id"] = self.year_group.id
        self.group = Group.objects.create(**group_data)

    # Test GET, POST on /users/year_groups/
    # Test PUT, DELETE on /users/year_groups/{id}/
    # Test GET, POST on /users/groups/
    # Test PUT, DELETE on /users/groups/{id}
    # Test PUT on /users/{id}/groups/{id}
    def test_create_and_delete_new_group(self):
        group_count = Group.objects.count()
        new_group_data = {"number": 2, 'year': self.year_group.id}
        url = "/api/v1/users/groups/"

        response = self.client.post(url, new_group_data, format="json")
        self.assertEqual(group_count + 1, Group.objects.count())
