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
        field_name = request.data.get("field_name")
        roll_type = request.data.get("roll_type")
        roll_scope = request.data.get("roll_scope")  # group roll or individual creature roll?

        if not field_name:
            return Response(
                status=406, data={"error": "missing field_name"}
            )

        if roll_scope == "individual" or roll_scope is None:
            creature_id = request.data.get("creature_id")

            if not creature_id:
                return Response(
                    status=406, data={"error": "missing creature_id"}
                )

            try:
                creature = models.Creature.objects.get(pk=creature_id)
            except models.Creature.DoesNotExist:
                return Response(
                    status=404, data={"error": f"creature with id: {creature_id} not found"}
                )

            try:
                rolls = {
                    f"{creature.id}": {
                        f"{field_name}": creature.roll(field_name=field_name, roll_type=roll_type)
                    }
                }
            except AttributeError:
                return Response(
                    status=406, data={"error": f"field_name: {field_name} is not valid"}
                )
        else:  # Else this is a group roll type, so there should be an encounter id instead of a creature id
            encounter_id = request.data.get("encounter_id")
            if not encounter_id:
                return Response(
                    status=406, data={"error": "missing encounter_id"}
                )
            try:
                creatures = models.Encounter.objects.get(pk=encounter_id).creatures.all()
            except models.Encounter.DoesNotExist:
                return Response(
                    status=400, data={"error": f"Encounter {encounter_id} does not exist."}
                )
            rolls = {}
            for creature in creatures:
                # This is way overkill for just a single field, but it gives us room if we want to expand later
                rolls[f"{creature.id}"] = {
                        f"{field_name}": creature.roll(field_name=field_name, roll_type=roll_type)
                    }

        content = {"results": rolls}
        return Response(content)
