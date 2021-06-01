# Generated by Django 3.2.3 on 2021-05-20 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GrowUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True, null=True)),
                ('wait_interval', models.IntegerField()),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('plant', models.CharField(blank=True, max_length=255, null=True)),
                ('enabled', models.BooleanField(default=False)),
                ('auto_water', models.BooleanField(default=True)),
                ('alarm', models.BooleanField(default=False)),
                ('wet_point', models.DecimalField(decimal_places=1, max_digits=3)),
                ('dry_point', models.DecimalField(decimal_places=1, max_digits=3)),
                ('alarm_point', models.DecimalField(decimal_places=1, max_digits=3)),
                ('pump_speed', models.DecimalField(decimal_places=1, max_digits=3)),
                ('pump_duration', models.DecimalField(decimal_places=1, max_digits=3)),
                ('grow_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grow_api.growunit')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
    ]