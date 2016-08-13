import random

from django.db import models

class RoomData(models.Model):
    """
    A way to store the useful lookup data for particular rooms.
    """

    description = models.TextField(default=None, null=True)
    seed = models.CharField(max_length=255)
    area = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

