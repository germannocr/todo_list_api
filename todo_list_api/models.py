from django.db import models


class Card(models.Model):
    """
    The Card represents a task.
    """

    class Meta:

        db_table = 'card'

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=120)
    status = models.CharField(max_length=20)
    created_by_user = models.IntegerField()