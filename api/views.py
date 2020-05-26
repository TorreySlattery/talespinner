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
        creature_id = request.data.get("creature_id")
        field_name = request.data.get("field_name")
        if not creature_id or not field_name:
            return Response(
                status=406, data={"error": "missing creature_id and/or field_name"}
            )

        try:
            creature = models.Creature.objects.get(pk=creature_id)
        except models.Creature.DoesNotExist:
            return Response(
                status=404, data={"error": f"creature with id: {creature_id} not found"}
            )

        try:
            roll = creature.roll(field_name)
        except AttributeError:
            return Response(
                status=406, data={"error": f"field_name: {field_name} is not valid"}
            )

        content = {"result": roll}
        return Response(content)
