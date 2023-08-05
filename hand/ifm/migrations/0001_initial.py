# Generated by Django 3.2 on 2023-08-05 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UseWordCard',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('img', models.CharField(max_length=100)),
                ('word', models.CharField(max_length=10)),
                ('upload_date', models.DateTimeField(default=False)),
                ('user_id_ifm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reg.userifm', to_field='id')),
            ],
        ),
        migrations.CreateModel(
            name='UserDefIfm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('headimg', models.CharField(max_length=100)),
                ('describe', models.CharField(max_length=256)),
                ('score', models.FloatField(default=0.0, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ifm_user', to='reg.userifm', to_field='id')),
            ],
        ),
    ]
