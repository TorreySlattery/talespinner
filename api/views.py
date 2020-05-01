from rest_framework import viewsets

from creatures import models
from api import serializers


class EncounterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Encounter.objects.all()
    serializer_class = serializers.EncounterSerializer