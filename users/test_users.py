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


group_data = {"number": 3}

year_group_data = {"year": 2017, "type": 1}


class TestGroups(APITestCase):
    def setUp(self):
        self.year_group = YearGroup.objects.create(**year_group_data)
        group_data["study_year_id"] = self.year_group.id
        self.group = Group.objects.create(**group_data)

    # Test GET(200), POST (201, 400) on /users/year_groups/
    # Test PUT(200, 400, 404), DELETE(200, 404) on /users/year_groups/{id}/
    # Test POST(400) on /users/groups/
    # Test PUT(200, 400, 404), DELETE(404) on /users/groups/{id}
    # Test PUT(200, 400, 404) on /users/{id}/groups/{id}
    # TEST GET(200, 404) on /users/{id}/groups/

    def test_view_before_create_and_delete_group(self):
        # Tests GET(200) on /users/groups/
        # Tests POST (201) on /users/groups
        # Tests DELETE (200) on /users/groups/{id}
        group_count = Group.objects.count()
        new_group_data = {"number": 2, "year_id": self.year_group.id}
        url = reverse('group-list')
        response_get = self.client.get(url, {}, format="json")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), group_count)

        response_post = self.client.post(url, new_group_data, format="json")
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(group_count + 1, Group.objects.count())

        response_get = self.client.get(url, {}, format="json")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), Group.objects.count())

        url = reverse('group-detail', args=(response_post.data['id'],))
        response_delete = self.client.delete(url, {}, format="json")
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete.data['id'], response_post.data['id'])
        self.assertEqual(group_count, Group.objects.count())
