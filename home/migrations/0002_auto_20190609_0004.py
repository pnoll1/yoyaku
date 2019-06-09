# Generated by Django 2.2.1 on 2019-06-09 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_by_user', models.TextField()),
                ('name_reservation', models.TextField()),
                ('name_restaurant', models.TextField()),
                ('party_size', models.IntegerField()),
                ('time', models.TimeField()),
                ('caller', models.TextField()),
                ('request_completed', models.BooleanField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='place',
            options={'managed': False},
        ),
    ]
