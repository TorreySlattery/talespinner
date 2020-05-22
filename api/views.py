from rest_framework import viewsets

from creatures import models
from api import serializers


class EncounterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Encounter.objects.all().prefetch_related(
        "creatures",
        "creatures__template",
        "creatures__template__senses",
        "creatures__template__languages",
        "creatures__template__traits",
        "creatures__template__race"
    )
    serializer_class = serializers.EncounterSerializer
