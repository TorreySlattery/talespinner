# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 04:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ConditionImmunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Creature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('armor_class', models.PositiveSmallIntegerField()),
                ('hit_points', models.PositiveSmallIntegerField()),
                ('speed', models.PositiveSmallIntegerField()),
                ('strength', models.PositiveSmallIntegerField()),
                ('dexterity', models.PositiveSmallIntegerField()),
                ('constitution', models.PositiveSmallIntegerField()),
                ('intelligence', models.PositiveSmallIntegerField()),
                ('wisdom', models.PositiveSmallIntegerField()),
                ('charisma', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DamageImmunity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DefensiveAbility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=50)),
                ('amount', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='KillableCreature',
            fields=[
                ('creature_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bestiary.Creature')),
                ('challenge_rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('experience_worth', models.PositiveIntegerField()),
            ],
            bases=('bestiary.creature',),
        ),
        migrations.AddField(
            model_name='sense',
            name='creatures',
            field=models.ManyToManyField(to='bestiary.Creature'),
        ),
        migrations.AddField(
            model_name='language',
            name='creatures',
            field=models.ManyToManyField(to='bestiary.Creature'),
        ),
        migrations.AddField(
            model_name='damageimmunity',
            name='creatures',
            field=models.ManyToManyField(to='bestiary.Creature'),
        ),
        migrations.AddField(
            model_name='creature',
            name='alignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bestiary.Alignment'),
        ),
        migrations.AddField(
            model_name='creature',
            name='genus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bestiary.Genus'),
        ),
        migrations.AddField(
            model_name='creature',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bestiary.Size'),
        ),
        migrations.AddField(
            model_name='conditionimmunity',
            name='creatures',
            field=models.ManyToManyField(to='bestiary.Creature'),
        ),
    ]
