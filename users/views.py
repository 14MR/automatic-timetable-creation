from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from users.serializers import AuthTokenSerializer, SignupSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class ObtainAuthTokenEmail(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])

        return Response({
            'token': token.key
        })


class SignupApiView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)