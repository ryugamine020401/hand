# Generated by Django 3.2 on 2023-08-25 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0005_rename_teach_teachtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test1',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='test1ans',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='test2',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='test2ans',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
