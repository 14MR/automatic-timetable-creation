from django.db.models import Max
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from classes.factory import SemesterFactory, CourseFactory, ClassFactory
from classes.models import Semester, Course, Class, ClassType
from users.factory import GroupFactory
from users.models import Group


class TestSemesters(APITestCase):
    def setUp(self):
        self.semester = SemesterFactory.create_batch(size=1)[0]

    def test_view_semester(self):
        # Tests GET(200) on /classes/semesters/
        semester_count = Semester.objects.count()
        url = reverse("semester-list")
        response_get = self.client.get(url)

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data['results']), semester_count)

    def test_create_semester(self):
        # Tests POST (201) on /classes/semesters/
        semester_count = Semester.objects.count()
        new_semester_data = {"year": 2017, "type": 0}
        url = reverse("semester-list")

        response_post = self.client.post(url, new_semester_data, format="json")
        response_get = self.client.get(url)

        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(semester_count + 1, Semester.objects.count())
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data['results']), Semester.objects.count())

    def test_delete_semester(self):
        # Tests DELETE (200) on /classes/semesters/
        semester_count = Semester.objects.count()
        semester = SemesterFactory.create_batch(size=1)[0]
        url = reverse("semester-detail", args=(semester.id,))
        response_delete = self.client.delete(url)

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete.data["id"], semester.id)
        self.assertEqual(semester_count, Semester.objects.count())

    def test_put_semester(self):
        # Test PUT(200) on /classes/semesters/{id}/
        new_semester_data = {"year": 2018, "type": self.semester.type}
        url = reverse("semester-detail", args=(self.semester.id,))
        response = self.client.put(url, new_semester_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["year"], new_semester_data["year"])
        self.assertEqual(
            Semester.objects.get(pk=self.semester.id).year, new_semester_data["year"]
        )

    def test_view_single_semester(self):
        # Tests GET(200) on /classes/semesters/{id}/
        url = reverse("semester-detail", args=(self.semester.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["year"], self.semester.year)

    def test_erroneous_get_semester(self):
        # Tests GET(404) on /classes/semesters/{id}/
        max_id = Semester.objects.all().aggregate(Max("id"))["id__max"] + 1

        url = reverse("semester-detail", args=(max_id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_post_semester(self):
        # Tests POST(400) on /classes/semesters/
        semester_count = Semester.objects.count()
        url = reverse("semester-list")
        new_semester_data = {"year": 2018, "type": 1000}

        response_post = self.client.post(url, new_semester_data, format="json")
        self.assertEqual(response_post.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(semester_count, Semester.objects.count())

    def test_erroneous_put_semester(self):
        # Tests PUT(400,404) on /classes/semesters/{id}/
        new_semester_data = {"type": 1000}

        url = reverse("semester-detail", args=(self.semester.id,))
        response_put = self.client.put(url, new_semester_data, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_400_BAD_REQUEST)

        max_id = Semester.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("semester-detail", args=(max_id,))
        response_put = self.client.put(url, new_semester_data, format="json")

        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_delete_semester(self):
        # Tests DELETE(404) on /classes/semesters/{id}/
        max_id = Semester.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("semester-detail", args=(max_id,))

        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)


class TestCourses(APITestCase):
    def setUp(self):
        self.course = CourseFactory.create_batch(size=1)[0]

    def test_view_course(self):
        # Tests GET(200) on /classes/courses/
        course_count = Course.objects.count()
        url = reverse("course-list")
        response_get = self.client.get(url)

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data['results']), course_count)

    def test_create_course(self):
        # Tests POST (201) on /classes/courses/
        course_count = Course.objects.count()
        new_course_data = {
            "title": "Linear Algebra",
            "description": "Delve into the N-space",
            "semester_id": self.course.semester_id,
            "year_group_id": self.course.year_group_id,
        }
        url = reverse("course-list")

        response_post = self.client.post(url, new_course_data, format="json")
        response_get = self.client.get(url)

        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(course_count + 1, Course.objects.count())
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data['results']), Course.objects.count())

    def test_delete_course(self):
        # Tests DELETE (200) on /classes/courses/
        course_count = Course.objects.count()
        course = CourseFactory.create_batch(size=1)[0]
        url = reverse("course-detail", args=(course.id,))
        response_delete = self.client.delete(url)

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete.data["id"], course.id)
        self.assertEqual(course_count, Course.objects.count())

    def test_put_course(self):
        # Test PUT(200) on /classes/courses/{id}/
        new_course_data = {
            "title": "Not A Linear Algebra",
            "description": self.course.description,
            "semester_id": self.course.semester_id,
            "year_group_id": self.course.year_group_id,
        }
        url = reverse("course-detail", args=(self.course.id,))
        response = self.client.put(url, new_course_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], new_course_data["title"])
        self.assertEqual(
            Course.objects.get(pk=self.course.id).title, new_course_data["title"]
        )

    def test_view_single_course(self):
        # Tests GET(200) on /classes/courses/{id}/
        url = reverse("course-detail", args=(self.course.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.course.title)

    def test_erroneous_get_course(self):
        # Tests GET(404) on /classes/courses/{id}/
        max_id = Course.objects.all().aggregate(Max("id"))["id__max"] + 1

        url = reverse("course-detail", args=(max_id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_post_course(self):
        # Tests POST(400) on /classes/courses/
        course_count = Course.objects.count()
        url = reverse("course-list")
        new_course_data = {
            "title": "Not A Linear Algebra",
            "description": 405,
            "semester_id": -1,
            "year_group_id": self.course.year_group_id,
        }
        response_post = self.client.post(url, new_course_data, format="json")
        self.assertEqual(response_post.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(course_count, Course.objects.count())

    def test_erroneous_put_course(self):
        # Tests PUT(400,404) on /classes/courses/{id}/
        new_course_data = {"title": 0}

        url = reverse("course-detail", args=(self.course.id,))
        response_put = self.client.put(url, new_course_data, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_400_BAD_REQUEST)

        max_id = Course.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("course-detail", args=(max_id,))
        response_put = self.client.put(url, new_course_data, format="json")

        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_delete_course(self):
        # Tests DELETE(404) on /classes/courses/{id}/
        max_id = Course.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("course-detail", args=(max_id,))

        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)


class TestClasses(APITestCase):
    def setUp(self):
        self.this_class = ClassFactory.create_batch(size=1)[0]
        self.groups = GroupFactory.create_batch(size=3)

    def test_view_class(self):
        # Tests GET(200) on /classes/
        class_count = Class.objects.count()
        url = reverse("class-list")
        response_get = self.client.get(url)

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data['results']), class_count)

    def test_create_class(self):
        # Tests POST (201) on /classes/
        class_count = Class.objects.count()
        new_class_data = {
            "course_id": self.this_class.course_id,
            "type_id": self.this_class.type_id,
            "per_week": 1,
            "group_ids": [self.groups[0].id],
            "teacher_id": self.this_class.teacher_id,
        }
        url = reverse("class-list")

        response_post = self.client.post(url, new_class_data, format="json")
        response_get = self.client.get(url)

        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(class_count + 1, Class.objects.count())
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data['results']), Class.objects.count())

    def test_delete_class(self):
        # Tests DELETE (200) on /classes/
        class_count = Class.objects.count()
        current_class = ClassFactory.create_batch(size=1)[0]
        url = reverse("class-detail", args=(current_class.id,))
        response_delete = self.client.delete(url)

        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_delete.data["id"], current_class.id)
        self.assertEqual(class_count, Class.objects.count())

    def test_put_class(self):
        # Test PUT(200) on /classes/{id}/
        groups_id = list(map(lambda x: x.id, self.groups))
        new_class_data = {
            "course_id": self.this_class.course_id,
            "type_id": self.this_class.type_id,
            "per_week": 1,
            "group_ids": groups_id,
            "teacher_id": self.this_class.teacher_id,
        }
        url = reverse("class-detail", args=(self.this_class.id,))
        response = self.client.put(url, new_class_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["course_id"], new_class_data["course_id"])
        self.assertEqual(
            Class.objects.get(pk=self.this_class.id).course_id,
            new_class_data["course_id"],
        )
        self.assertEqual(response.data["group_ids"], groups_id)

    def test_view_single_class(self):
        # Tests GET(200) on /classes/{id}/
        url = reverse("class-detail", args=(self.this_class.id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["course_id"], self.this_class.course_id)

    def test_erroneous_get_class(self):
        # Tests GET(404) on /classes/{id}/
        max_id = Class.objects.all().aggregate(Max("id"))["id__max"] + 1

        url = reverse("class-detail", args=(max_id,))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_post_class(self):
        # Tests POST(400) on /classes/
        class_count = Class.objects.count()
        url = reverse("class-list")
        new_class_data = {
            "course_id": self.this_class.course_id,
            "type_id": self.this_class.type_id,
            "per_week": 1,
            "group_ids": [Group.objects.all().aggregate(Max("id"))["id__max"] + 1],
            "teacher_id": self.this_class.teacher_id,
        }
        response_post = self.client.post(url, new_class_data, format="json")
        self.assertEqual(response_post.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(class_count, Class.objects.count())

    def test_erroneous_put_class(self):
        # Tests PUT(400,404) on /classes/{id}/
        new_class_data = {"title": 0}

        url = reverse("class-detail", args=(self.this_class.id,))
        response_put = self.client.put(url, new_class_data, format="json")
        self.assertEqual(response_put.status_code, status.HTTP_400_BAD_REQUEST)

        max_id = Class.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("class-detail", args=(max_id,))
        response_put = self.client.put(url, new_class_data, format="json")

        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

    def test_erroneous_delete_class(self):
        # Tests DELETE(404) on /classes/{id}/
        max_id = Class.objects.all().aggregate(Max("id"))["id__max"] + 1
        url = reverse("class-detail", args=(max_id,))

        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_class_types(self):
        # Tests GET(200) on /classes/types/
        class_type_count = ClassType.objects.count()
        url = reverse("class-types")
        response_get = self.client.get(url)

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_get.data), class_type_count)
