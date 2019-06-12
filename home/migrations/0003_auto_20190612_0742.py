# Generated by Django 2.2.1 on 2019-06-12 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20190609_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='caller',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='request_completed',
            field=models.BooleanField(blank=True),
        ),
        migrations.AlterModelTable(
            name='place',
            table='home_planet_osm_point',
        ),
    ]