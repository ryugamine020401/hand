# Generated by Django 3.2 on 2023-11-14 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserIfm',
            fields=[
                ('email', models.EmailField(max_length=100, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('id', models.IntegerField(default=0, unique=True)),
                ('validation', models.BooleanField(default=False)),
                ('validation_num', models.IntegerField(default=0)),
                ('birthday', models.DateField(default='1900-01-01')),
            ],
        ),
    ]
