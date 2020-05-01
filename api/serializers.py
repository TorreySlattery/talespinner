from rest_framework import serializers

from creatures import models


class EncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Encounter
        fields = ["name", "description",]