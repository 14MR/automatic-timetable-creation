from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from django.contrib.auth import authenticate

from users.models import User, Group, YearGroup


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        source="group", read_only=True
    )
    email = serializers.CharField(read_only=True)
    role = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "group_id", "role")


class UserCreateSerializer(UserSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    group_id = serializers.PrimaryKeyRelatedField(
        source="group", queryset=Group.objects.all(), required=False
    )
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", "group_id", "role")


class GroupSerializer(serializers.ModelSerializer):
    year_id = serializers.PrimaryKeyRelatedField(
        source="study_year", queryset=YearGroup.objects.all()
    )

    class Meta:
        model = Group
        fields = ("id", "number", "year_id")


class YearGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearGroup
        fields = ("id", "year", "type")
