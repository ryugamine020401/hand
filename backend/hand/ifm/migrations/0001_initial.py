# Generated by Django 3.2 on 2023-11-14 17:22

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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('img', models.ImageField(upload_to='')),
                ('word', models.CharField(max_length=10)),
                ('upload_date', models.DateTimeField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reg.userifm', to_field='id')),
            ],
        ),
        migrations.CreateModel(
            name='UserSignLanguageCard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('picurl', models.TextField(null=True)),
                ('videourl', models.TextField(null=True)),
                ('vocabularie', models.CharField(default='', max_length=50)),
                ('chinese', models.CharField(default='', max_length=255)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reg.userifm', to_field='id')),
            ],
        ),
        migrations.CreateModel(
            name='UserDefIfm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('headimg', models.ImageField(upload_to='headimage')),
                ('describe', models.TextField()),
                ('score', models.FloatField(default=0.0, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reg.userifm', to_field='id')),
            ],
        ),
    ]
