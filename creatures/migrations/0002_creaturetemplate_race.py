# Generated by Django 3.0.5 on 2020-05-22 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creatures', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creaturetemplate',
            name='race',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='creatures.Race'),
        ),
    ]