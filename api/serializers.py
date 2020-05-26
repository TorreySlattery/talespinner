from rest_framework import serializers

from creatures import models


class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trait
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = "__all__"


class SenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sense
        fields = "__all__"


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Race
        fields = "__all__"


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Action
        fields = "__all__"


class AttackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attack
        fields = "__all__"


class CreatureTemplateSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(read_only=True, many=True)
    senses = SenseSerializer(read_only=True, many=True)
    traits = TraitSerializer(read_only=True, many=True)
    race = RaceSerializer(read_only=True)
    actions = ActionSerializer(read_only=True, many=True)
    attacks = AttackSerializer(read_only=True, many=True)

    class Meta:
        model = models.CreatureTemplate
        fields = "__all__"


class CreatureSerializer(serializers.ModelSerializer):
    template = CreatureTemplateSerializer(read_only=True)

    class Meta:
        model = models.Creature
        fields = "__all__"


class EncounterSerializer(serializers.ModelSerializer):
    creatures = CreatureSerializer(read_only=True, many=True)

    class Meta:
        model = models.Encounter
        fields = "__all__"


class EncounterGroupSerializer(serializers.ModelSerializer):
    encounters = EncounterSerializer(read_only=True, many=True)

    class Meta:
        model = models.EncounterGroup
        fields = "__all__"
