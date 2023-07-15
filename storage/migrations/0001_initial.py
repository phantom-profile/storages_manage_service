# Generated by Django 4.2.2 on 2023-07-09 16:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('truck_id', models.UUIDField(default=uuid.UUID('c2f2fffb-a100-4339-986b-89bc07a80124'), unique=True)),
                ('capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('exploitation_start', models.DateTimeField()),
                ('exploitation_finish', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('current_storage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='storage.storage')),
            ],
        ),
    ]
