# Generated by Django 3.2 on 2023-08-12 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifm', '0003_alter_usewordcard_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usewordcard',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
