"""PyTest tests for 'users' application """
from django.db.models import Max
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, YearGroup, Group
from users.factory import YearGroupFactory, GroupFactory

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
        self.user = User.objects.create(email="test@test.com", is_active=True)

    def test_view_year_group(self):
        # Tests GET(200) on /users/year_groups/
        group_count = YearGroup.objects.count()
        url = reverse("year_group-list")
        response_get = self.client.get(url, {}, format="json")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), group_count)

    def test_create_year_group(self):
        # Tests POST (201) on /users/year_groups/
        group_count = YearGroup.objects.count()
        new_group_data = {"year": 2018, "type": 0}
        url = reverse("year_group-list")

        response_post = self.client.post(url, new_group_data, format="json")
        response_get = self.client.get(url, {}, format="json")

        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(group_count + 1, YearGroup.objects.count())
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), YearGroup.objects.count())

    def test_view_before_create_and_delete_year_group(self):
        # Tests DELETE (200) on /users/year_groups/{id}
        group_count = YearGroup.objects.count()
        year_group = YearGroupFactory.create_batch(size=1)[0]
        url = reverse("year_group-detail", args=(year_group.id,))
        response_delete = self.client.delete(url, {}, format="json")

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete.data["id"], year_group.id)
        self.assertEqual(group_count, YearGroup.objects.count())

    def test_erroneous_post_year_group(self):
        # Tests POST(400) on /users/year_groups/
        group_count = YearGroup.objects.count()
        url = reverse("year_group-list")
        new_group_data = {"year": 2018, "type": 3}

        response_post = self.client.post(url, new_group_data, format="json")
        self.assertEqual(response_post.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(group_count, YearGroup.objects.count())

    def test_erroneous_put_year_groups(self):
        # Tests PUT(400,404) on /users/year_groups/{id}/
        new_group_data = {"year": 2018, "type": 3}

        url = reverse("year_group-detail", args=(self.year_group.id,))
        response_put = self.client.put(url, new_group_data, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_400_BAD_REQUEST)

        max_id = YearGroup.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("year_group-detail", args=(max_id,))
        response_put = self.client.put(url, new_group_data, format="json")

        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_delete_year_groups(self):
        # Tests DELETE(404) on /users/year_groups/{id}/
        max_id = YearGroup.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("year_group-detail", args=(max_id,))

        response_delete = self.client.delete(url, {}, format="json")
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_year_group(self):
        # Test PUT(200) on /users/year_groups/{id}
        new_group_data = {"year": 2020, "type": 0}
        url = reverse("year_group-detail", args=(self.year_group.id,))
        response = self.client.put(url, new_group_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["year"], new_group_data["year"])
        self.assertEqual(
            YearGroup.objects.get(pk=self.year_group.id).year, new_group_data["year"]
        )

    def test_view_group(self):
        # Tests GET(200) on /users/groups/
        group_count = Group.objects.count()
        url = reverse("group-list")
        response_get = self.client.get(url, {}, format="json")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), group_count)

    def test_post_group(self):
        # Tests POST (201) on /users/groups
        group_count = Group.objects.count()
        new_group_data = {"number": 2, "year_id": self.year_group.id}
        url = reverse("group-list")

        response_post = self.client.post(url, new_group_data, format="json")
        response_get = self.client.get(url, {}, format="json")

        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(group_count + 1, Group.objects.count())
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), Group.objects.count())

    def test_view_before_create_and_delete_group(self):
        # Tests DELETE (200) on /users/groups/{id}
        group_count = Group.objects.count()
        group = GroupFactory.create_batch(size=1)[0]
        url = reverse("group-detail", args=(group.id,))

        response_delete = self.client.delete(url, {}, format="json")

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete.data["id"], group.id)
        self.assertEqual(group_count, Group.objects.count())

    def test_erroneous_post_groups(self):
        # Tests POST(400) on /users/groups/
        group_count = Group.objects.count()
        url = reverse("group-list")
        new_group_data = {"number": -1, "year_id": self.year_group.id}

        response_post = self.client.post(url, new_group_data, format="json")
        self.assertEqual(response_post.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(group_count, Group.objects.count())

    def test_erroneous_put_groups(self):
        # Tests PUT(400,404) on /users/groups/{id}/
        new_group_data = {"number": -1, "year_id": self.year_group.id}

        url = reverse("group-detail", args=(self.group.id,))
        response_put = self.client.put(url, new_group_data, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_400_BAD_REQUEST)

        max_id = Group.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("group-detail", args=(max_id,))
        new_group_data = {"number": 3, "year_id": self.year_group.id}
        response_put = self.client.put(url, new_group_data, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_delete_groups(self):
        # Tests DELETE(404) on /users/groups/{id}/
        max_id = Group.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("group-detail", args=(max_id,))

        response_delete = self.client.delete(url, {}, format="json")
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_put_to_user_group(self):
        # Tests PUT(404) on /users/{id}/groups/{id}/
        max_id = Group.objects.all().aggregate(Max("id"))["id__max"] + 1
        max_user_id = User.objects.all().aggregate(Max("id"))["id__max"] + 1

        url = reverse("users-add-group", args=(max_user_id, self.group.id))
        response_put = self.client.put(url, {}, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse("users-add-group", args=(self.user.id, max_id))
        response_put = self.client.put(url, {}, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_add_to_user_group(self):
        # Tests GET(404) on /users/{id}/groups/
        max_user_id = User.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("users-view-group", args=(max_user_id,))
        response_get = self.client.get(url, {}, format="json")

        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_group(self):
        # Test PUT(200) on /users/groups/{id}
        new_group_data = {"number": 100, "year_id": self.year_group.id}
        url = reverse("group-detail", args=(self.group.id,))
        response = self.client.put(url, new_group_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number"], new_group_data["number"])
        self.assertEqual(
            Group.objects.get(pk=self.group.id).number, new_group_data["number"]
        )
