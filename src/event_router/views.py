from rest_framework import viewsets, mixins
from rest_framework.response import Response

from crema.permissions import InternalTokenRequired
from event_router.serializers import EventSerializer


class EventRouterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = EventSerializer
    permission_classes = (InternalTokenRequired,)
