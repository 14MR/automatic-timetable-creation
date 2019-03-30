from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from classes.models import Class, Semester, Course
from classes.serializers import (
    ClassSerializer,
    ClassTypeSerializer,
    SemesterSerializer,
    CourseSerializer,
)


class ClassViewSet(viewsets.ModelViewSet):
    serializer_class = ClassSerializer
    permission_classes = [AllowAny]
    queryset = Class.objects.all()


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    queryset = Course.objects.all()


class SemesterViewSet(viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    permission_classes = [AllowAny]
    queryset = Semester.objects.all()
