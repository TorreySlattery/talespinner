from django.db import models


class CreatureTemplate(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    str = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    dex = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    con = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    int = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    wis = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    cha = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    speed = models.PositiveSmallIntegerField(null=False, blank=False, default=30)
    min_hp = models.PositiveSmallIntegerField(null=False, blank=False, default=1)
    max_hp = models.PositiveSmallIntegerField(null=False, blank=False, default=1000)


class StatusEffect(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)


class Creature(models.Model):
    template = models.ForeignKey(
        CreatureTemplate, related_name="creatures", on_delete=models.Cascade
    )
    current_hp = models.PositiveSmallIntegerField()
    status_effects = models.ManyToManyField(StatusEffect)
