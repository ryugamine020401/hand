# Generated by Django 3.2 on 2023-08-12 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ifm', '0004_alter_usewordcard_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usewordcard',
            old_name='user_id_ifm',
            new_name='user_id',
        ),
    ]