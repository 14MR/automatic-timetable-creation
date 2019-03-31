from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from schedule.serializers import Event, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)
    queryset = Event.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = EventSerializer(instance).data
        instance.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)
