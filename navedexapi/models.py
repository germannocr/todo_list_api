from django.db import models
from django.contrib.postgres.fields import ArrayField


class Naver(models.Model):

    class Meta:

        db_table = 'naver'

    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=60)
    birthdate = models.CharField(max_length=10)
    admission_date = models.CharField(max_length=10)
    job_role = models.CharField(max_length=120)
    projects = ArrayField(models.IntegerField(null=True, blank=True))
    created_by_user = models.IntegerField()

    def __str__(self):
        return f'{self.name} '


class Project(models.Model):

    class Meta:
        db_table = 'post'

    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=120)
    navers = ArrayField(models.IntegerField(null=True, blank=True))


    def __str__(self):
        return f'{self.name}'
