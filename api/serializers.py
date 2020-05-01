from rest_framework import serializers

from creatures import models


class CreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Creature
        fields = "__all__"


class EncounterSerializer(serializers.ModelSerializer):
    creatures = CreatureSerializer(read_only=True, many=True)

    class Meta:
        model = models.Encounter
        fields = "__all__"
