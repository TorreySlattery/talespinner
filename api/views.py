from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from creatures import models
from api import serializers


class EncounterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Encounter.objects.all().prefetch_related(
        "creatures",
        "creatures__template",
        "creatures__template__senses",
        "creatures__template__languages",
        "creatures__template__traits",
        "creatures__template__race",
    )
    serializer_class = serializers.EncounterSerializer


class EncounterGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.EncounterGroup.objects.all().prefetch_related(
        "encounters",
        "encounters__creatures",
        "encounters__creatures__template",
        "encounters__creatures__template__senses",
        "encounters__creatures__template__languages",
        "encounters__creatures__template__traits",
        "encounters__creatures__template__race",
    )

    serializer_class = serializers.EncounterGroupSerializer


class RollView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        content = {
            "Hey": "there Kadala {}".format(request.data)
        }
        return Response(content)
