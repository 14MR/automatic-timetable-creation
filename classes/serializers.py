from rest_framework import serializers
from classes.models import Class, ClassType, Course, Semester
from users.models import YearGroup, User, Group


class ClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassType
        fields = ("id", "title")


class ClassSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(
        source="course", queryset=Course.objects.all()
    )
    type_id = serializers.PrimaryKeyRelatedField(
        source="type", queryset=ClassType.objects.all()
    )
    teacher_id = serializers.PrimaryKeyRelatedField(
        source="teacher", queryset=User.objects.all()
    )  # TODO: ADD roles
    group_ids = serializers.PrimaryKeyRelatedField(
        source="groups", queryset=Group.objects.all(), many=True
    )

    class Meta:
        model = Class
        fields = ("id", "course_id", "type_id", "per_week", "group_ids", "teacher_id")


class CourseSerializer(serializers.ModelSerializer):
    semester_id = serializers.PrimaryKeyRelatedField(
        source="semester", queryset=Semester.objects.all()
    )
    year_group_id = serializers.PrimaryKeyRelatedField(
        source="year_group", queryset=YearGroup.objects.all()
    )

    class Meta:
        model = Course
        fields = ("id", "title", "description", "semester_id", "year_group_id")


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ("id", "year", "type")
