# Generated by Django 3.2 on 2023-08-24 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20230823_2349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discussresponse',
            old_name='user_id_forum',
            new_name='user_id',
        ),
    ]
