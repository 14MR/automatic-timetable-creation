from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from users.models import User, Group, YearGroup
from users.serializers import (
    AuthTokenSerializer,
    UserSerializer,
    GroupSerializer,
    YearGroupSerializer,
)


class ObtainAuthTokenEmail(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(
            user=serializer.validated_data["user"]
        )

        return Response({"token": token.key})


class SignupApiView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class ProfileApiView(APIView):
    def put(self, request, *args, **kwargs):
        request.data["id"] = request.user.id
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)
    queryset = Group.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = GroupSerializer(instance).data
        instance.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class YearGroupViewSet(viewsets.ModelViewSet):
    serializer_class = YearGroupSerializer
    permission_classes = (AllowAny,)
    queryset = YearGroup.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = YearGroupSerializer(instance).data
        instance.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class UserGroupAdd(UpdateAPIView):
    permission_classes = (AllowAny,)

    def put(self, request, user_id, group_id, *args, **kwargs):
        user = get_object_or_404(User, pk=user_id)
        group = get_object_or_404(Group, pk=group_id)
        user.group_id = group.id
        user.save()
        return Response(status=status.HTTP_200_OK)


class UserGroupView(RetrieveAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, user_id, *args, **kwargs):

        user = get_object_or_404(User, pk=user_id)
        serializer = GroupSerializer(user.group)
        return Response(serializer.data, status=status.HTTP_200_OK)
