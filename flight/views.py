import datetime
from rest_framework import viewsets, mixins, permissions

from .models import *
from .serializers import *



class FlightTicketViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    API endpoint that allows SuperAdmin to see and work with therapies.
    """

    queryset = FlightTicket.objects.all()
    serializer_class = FlightTicketSerializer
    permission_classes = [permissions.AllowAny,]
