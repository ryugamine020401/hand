# Generated by Django 3.2 on 2023-08-09 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Billboard',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('context', models.TextField()),
                ('upload_date', models.DateField(default=False)),
            ],
        ),
    ]
