# Generated by Django 2.2.1 on 2019-08-03 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_place_staging'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place_staging',
            name='city',
        ),
        migrations.RemoveField(
            model_name='place_staging',
            name='cuisine',
        ),
        migrations.RemoveField(
            model_name='place_staging',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='place_staging',
            name='opening_hours',
        ),
        migrations.RemoveField(
            model_name='place_staging',
            name='outdoor_seating',
        ),
        migrations.RemoveField(
            model_name='place_staging',
            name='website',
        ),
    ]