# Generated by Django 2.2.1 on 2019-06-21 18:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20190616_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
