# Generated by Django 3.2 on 2023-08-09 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdefifm',
            name='headimg',
            field=models.ImageField(upload_to='headimage'),
        ),
    ]
