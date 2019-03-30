from rest_framework import generics, mixins, permissions
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import UpdateModelMixin
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from users.models import User
from users.serializers import AuthTokenSerializer, UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


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
    permission_classes = ()
    
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
