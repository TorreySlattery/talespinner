from random import randint

from django.db import models


ALIGNMENT_CHOICES = [
    ("LG", "Lawful Good"),
    ("LN", "Lawful Neutral"),
    ("LE", "Lawful Evil"),
    ("NG", "Neutral Good"),
    ("N", "Neutral"),
    ("NE", "Neutral Evil"),
    ("CG", "Chaotic Good"),
    ("CN", "Chaotic Neutral"),
    ("CE", "Chaotic Evil"),
    ("U", "Unaligned"),
]

SIZE_CHOICES = [
    ("T", "Tiny"),
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("H", "Huge"),
    ("C", "Colossal"),
    ("G", "Gargantuan"),
]

DAMAGE_CHOICIES = [
    ("acid", "acid"),
    ("bludgeoning", "bludgeoning"),
    ("cold", "cold"),
    ("fire", "fire"),
    ("force", "force"),
    ("lightning", "lightning"),
    ("necrotic", "necrotic"),
    ("piercing", "piercing"),
    ("poison", "poison"),
    ("slashing", "slashing"),
    ("thunder", "thunder"),
]


class Race(models.Model):
    type = models.CharField(max_length=255, null=False, blank=False)
    subtype = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = (
            "type",
            "subtype",
        )

    def __str__(self):
        return f"{self.type} ({self.subtype})" if self.subtype else f"{self.type}"


class Language(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name


class Trait(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name


class Sense(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    range = models.PositiveSmallIntegerField(null=False, blank=False, default=60)

    class Meta:
        unique_together = (
            "name",
            "range",
        )

    def __str__(self):
        return f"{self.name} {self.range}'"


class Condition(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class EncounterGroup(models.Model):
    """A way to group multiple encounters into one thematic idea, such as various small encounters in bandit hideout"""

    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name


class Encounter(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    encounter_group = models.ForeignKey(
        EncounterGroup,
        on_delete=models.SET_NULL,
        related_name="encounters",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class CreatureTemplate(models.Model):
    ALIGNMENT_CHOICES = ALIGNMENT_CHOICES + [
        ("A", "Any alignment"),
        ("AG", "Any Good"),
        ("AE", "Any Evil"),
        ("ANL", "Any non-lawful"),
    ]
    STR_FIELDS = ["str_save", "athletics"]
    DEX_FIELDS = ["dex_save", "acrobatics", "sleight_of_hand", "stealth"]
    CON_FIELDS = ["con_save"]
    INT_FIELDS = [
        "int_save",
        "arcana",
        "history",
        "investigation",
        "nature",
        "religion",
    ]
    WIS_FIELDS = [
        "wis_save",
        "animal_handling",
        "insight",
        "medicine",
        "perception",
        "survival",
    ]
    CHA_FIELDS = ["cha_save", "deception", "intimidation", "performance", "persuasion"]

    name = models.CharField(max_length=255, null=False, blank=False)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES, default="M")
    race = models.ForeignKey(Race, null=True, blank=True, on_delete=models.SET_NULL)
    str = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    dex = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    con = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    int = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    wis = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    cha = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    speed = models.PositiveSmallIntegerField(null=False, blank=False, default=30)
    min_hp = models.PositiveSmallIntegerField(null=False, blank=False, default=1)
    avg_hp = models.PositiveSmallIntegerField(
        null=False, blank=False, default=50, help_text="The listed health"
    )
    max_hp = models.PositiveSmallIntegerField(null=False, blank=False, default=1000)
    alignment = models.CharField(max_length=3, choices=ALIGNMENT_CHOICES, default="A")
    challenge_rating = models.FloatField(null=False, blank=False, default=1)
    experience = models.PositiveIntegerField(null=False, blank=False, default=0)
    ac = models.PositiveSmallIntegerField(null=False, blank=False, default=10)
    languages = models.ManyToManyField(Language)
    senses = models.ManyToManyField(Sense)
    traits = models.ManyToManyField(Trait, blank=True)

    acrobatics = models.SmallIntegerField(null=False, blank=False, default=0)
    animal_handling = models.SmallIntegerField(null=False, blank=False, default=0)
    arcana = models.SmallIntegerField(null=False, blank=False, default=0)
    athletics = models.SmallIntegerField(null=False, blank=False, default=0)
    deception = models.SmallIntegerField(null=False, blank=False, default=0)
    history = models.SmallIntegerField(null=False, blank=False, default=0)
    insight = models.SmallIntegerField(null=False, blank=False, default=0)
    intimidation = models.SmallIntegerField(null=False, blank=False, default=0)
    investigation = models.SmallIntegerField(null=False, blank=False, default=0)
    medicine = models.SmallIntegerField(null=False, blank=False, default=0)
    nature = models.SmallIntegerField(null=False, blank=False, default=0)
    perception = models.SmallIntegerField(null=False, blank=False, default=0)
    performance = models.SmallIntegerField(null=False, blank=False, default=0)
    persuasion = models.SmallIntegerField(null=False, blank=False, default=0)
    religion = models.SmallIntegerField(null=False, blank=False, default=0)
    sleight_of_hand = models.SmallIntegerField(null=False, blank=False, default=0)
    stealth = models.SmallIntegerField(null=False, blank=False, default=0)
    survival = models.SmallIntegerField(null=False, blank=False, default=0)

    str_save = models.SmallIntegerField(null=False, blank=False, default=0)
    dex_save = models.SmallIntegerField(null=False, blank=False, default=0)
    con_save = models.SmallIntegerField(null=False, blank=False, default=0)
    int_save = models.SmallIntegerField(null=False, blank=False, default=0)
    wis_save = models.SmallIntegerField(null=False, blank=False, default=0)
    cha_save = models.SmallIntegerField(null=False, blank=False, default=0)
    condition_immunities = models.ManyToManyField(Condition, blank=True)

    def __str__(self):
        return self.name

    def save(self):
        if not self.pk:
            for stat in ["str", "dex", "con", "int", "wis", "cha"]:
                fields_list = stat.upper() + "_FIELDS"
                for field in getattr(self, fields_list):
                    mod = (getattr(self, stat) - 10) // 2
                    # Only calculate if user didn't enter anything
                    if not getattr(self, field):
                        setattr(self, field, mod)
        super().save()


class Action(models.Model):
    """A human-readable list of things from the stat block."""

    template = models.ForeignKey(
        CreatureTemplate,
        null=True,
        blank=False,
        related_name="actions",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Attack(models.Model):
    """A collection of data to represent attacks from the Actions block."""

    template = models.ForeignKey(
        CreatureTemplate,
        null=True,
        blank=False,
        related_name="attacks",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True)
    to_hit_mod = models.PositiveSmallIntegerField(blank=False, null=False, default=3)
    num_dice = models.PositiveSmallIntegerField(blank=False, null=False, default=1)
    die_step = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        default=6,
        help_text="Basically the number of sides on the die",
    )
    dmg_mod = models.SmallIntegerField(blank=False, null=False, default=2)
    dmg_avg = models.SmallIntegerField(
        blank=False,
        null=False,
        default=4,
        help_text="For when people don't like rolling.",
    )
    dmg_type = models.CharField(max_length=255, choices=DAMAGE_CHOICIES)
    dmg_is_magic = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return f"{self.name} ({self.template})"


class Creature(models.Model):
    template = models.ForeignKey(
        CreatureTemplate, related_name="creatures", on_delete=models.CASCADE
    )
    display_name = models.CharField(max_length=255)
    current_hp = models.PositiveSmallIntegerField(default=50)
    conditions = models.ManyToManyField(Condition, blank=True)
    alignment = models.CharField(max_length=3, choices=ALIGNMENT_CHOICES, default="A")
    encounter = models.ForeignKey(
        Encounter,
        related_name="creatures",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    current_initiative = models.SmallIntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return f"{self.display_name} ({self.template.name})"

    def roll(self, field_name, roll_type=None):
        """
        Takes a field name and a type of roll (stat, skill, save; initiative is consider a stat roll), rolls 2 d20s
        and returns both results as a tuple for consumption.
        """
        field_name = field_name.lower()
        try:
            if roll_type == "stat":
                stat = getattr(self.template, field_name)
                mod = (stat - 10) // 2
            elif roll_type == "save":
                mod = getattr(self.template, field_name)
            elif roll_type == "skill":
                mod = getattr(self.template, field_name)
            else:
                mod = 0
        except AttributeError:
            raise
        roll_1 = randint(1, 20)
        roll_1_total = roll_1 + mod
        roll_2 = randint(1, 20)
        roll_2_total = roll_2 + mod

        mod_symbol = "+" if mod >= 0 else ""
        return (
            f"{roll_1}{mod_symbol}{mod}={roll_1_total}",
            f"{roll_2}{mod_symbol}{mod}={roll_2_total}",
        )


class CreatureHistory(models.Model):
    """A simple log for keeping track of what rolls a creature makes"""

    entry = models.TextField()
    creature = models.ForeignKey(
        Creature, null=False, blank=False, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
