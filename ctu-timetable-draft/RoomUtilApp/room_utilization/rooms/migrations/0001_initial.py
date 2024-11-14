# Generated by Django 5.1.2 on 2024-10-16 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.IntegerField(primary_key=True, serialize=False)),
                ('building_id', models.IntegerField()),
                ('campus_id', models.IntegerField()),
                ('room_number', models.CharField(max_length=50)),
                ('room_type', models.CharField(max_length=50)),
                ('availability_days', models.JSONField(default=list)),
                ('availability_times', models.JSONField(default=list)),
            ],
            options={
                'db_table': 'room',
                'managed': False,
            },
        ),
    ]
