from django.conf.urls import url, include
from rest_framework import routers

from classes.views import ClassViewSet, SemesterViewSet, CourseViewSet

router = routers.DefaultRouter()
router.register(r"semesters", SemesterViewSet, basename="semester")
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"", ClassViewSet, basename="class")

urlpatterns = [url(r"^", include(router.urls), name="classes")]
