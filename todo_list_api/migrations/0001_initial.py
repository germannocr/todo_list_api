# Generated by Django 3.1 on 2020-09-14 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=120)),
                ('status', models.CharField(max_length=20)),
                ('created_by_user', models.IntegerField()),
            ],
            options={
                'db_table': 'card',
            },
        ),
    ]
