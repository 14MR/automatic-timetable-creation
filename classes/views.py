from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from classes.models import Class, Semester, Course, ClassType
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = ClassSerializer(instance).data
        instance.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def types(self, request, pk=None):
        queryset = ClassType.objects.all()
        return Response(ClassTypeSerializer(queryset, many=True).data, status=status.HTTP_200_OK)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    queryset = Course.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = CourseSerializer(instance).data
        instance.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class SemesterViewSet(viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    permission_classes = [AllowAny]
    queryset = Semester.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = SemesterSerializer(instance).data
        instance.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)
