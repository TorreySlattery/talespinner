from django.db import models

class Size(models.Model):
    text = models.CharField(max_length=200)

class Alignment(models.Model):
    text = models.CharField(max_length=200)

class Genus(models.Model):
    text = models.CharField(max_length=200)

class Creature(models.Model):
    name = models.CharField(max_length=200)
    size = models.ForeignKey(Size)
    alignment = models.ForeignKey(Alignment)
    genus = models.ForeignKey(Genus)
    armor_class = models.PositiveSmallIntegerField()
    hit_points = models.PositiveSmallIntegerField()
    speed = models.PositiveSmallIntegerField()
    strength = models.PositiveSmallIntegerField()
    dexterity = models.PositiveSmallIntegerField()
    constitution = models.PositiveSmallIntegerField()
    intelligence = models.PositiveSmallIntegerField()
    wisdom = models.PositiveSmallIntegerField()
    charisma  = models.PositiveSmallIntegerField()

class KillableCreature(Creature):
    challenge_rating = models.DecimalField(decimal_places=2, max_digits=3)
    experience_worth = models.PositiveIntegerField()

class DamageImmunity(models.Model):
    text = models.CharField(max_length=50)
    creatures = models.ManyToManyField(Creature)

class ConditionImmunity(models.Model):
    text = models.CharField(max_length=50)
    creatures = models.ManyToManyField(Creature)

class Sense(models.Model):
    text = models.CharField(max_length=50)
    amount = models.PositiveSmallIntegerField()
    creatures = models.ManyToManyField(Creature)

class Language(models.Model):
    text = models.CharField(max_length=100)
    creatures = models.ManyToManyField(Creature)

class DefensiveAbility(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
