# Generated by Django 3.2 on 2023-08-09 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reg', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeachWordCard',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('img', models.CharField(max_length=100)),
                ('upload_date', models.DateField(default='1900-01-01')),
                ('describe', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Test1',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('mondai', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Test2',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('mondai', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Test2Ans',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('kotae_ichi', models.CharField(max_length=20)),
                ('kotae_ni', models.CharField(max_length=20)),
                ('kotae_san', models.CharField(max_length=20)),
                ('kotae_yon', models.CharField(max_length=20)),
                ('kotae_go', models.CharField(max_length=20)),
                ('cor_rate', models.FloatField(default=100.0)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reg.userifm', to_field='id')),
            ],
        ),
        migrations.CreateModel(
            name='Test1Ans',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('kotae_ichi', models.CharField(max_length=20)),
                ('kotae_ni', models.CharField(max_length=20)),
                ('kotae_san', models.CharField(max_length=20)),
                ('kotae_yon', models.CharField(max_length=20)),
                ('kotae_go', models.CharField(max_length=20)),
                ('cor_rate', models.FloatField(default=100.0)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reg.userifm', to_field='id')),
            ],
        ),
    ]