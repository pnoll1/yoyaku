# Generated by Django 2.2.1 on 2019-05-17 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('name_en', models.TextField(blank=True)),
                ('city', models.TextField()),
                ('cuisine', models.TextField(blank=True)),
                ('hours', models.TextField(blank=True)),
                ('english_friendly', models.BooleanField(blank=True)),
                ('outdoor_seating', models.BooleanField(blank=True)),
                ('website', models.TextField(blank=True)),
                ('menu', models.TextField(blank=True)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
            ],
        ),
    ]
