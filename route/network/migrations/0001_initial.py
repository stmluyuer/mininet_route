# Generated by Django 5.0.6 on 2024-05-14 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LinkData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100)),
                ('bw', models.FloatField()),
                ('delay', models.CharField(max_length=50)),
                ('loss', models.FloatField()),
                ('jitter', models.CharField(max_length=50)),
                ('error', models.FloatField()),
                ('max_queue_size', models.IntegerField()),
                ('rate', models.FloatField()),
                ('mtu', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
