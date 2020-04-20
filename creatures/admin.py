from django.contrib import admin
from creatures import models


class CreatureInline(admin.TabularInline):
    model = models.Creature
    extra = 0


@admin.register(models.Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    inlines = (CreatureInline,)


@admin.register(models.CreatureTemplate)
class CreatureTemplateAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Creature)
class CreatureAdmin(admin.ModelAdmin):
    list_display = ("display_name",)


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Sense)
class SenseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "range",
    )


@admin.register(models.Trait)
class TraitAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )


@admin.register(models.Attack)
class AttackAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
