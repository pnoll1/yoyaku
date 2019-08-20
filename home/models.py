from django.contrib.gis.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
import uuid

class place(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    name_en = models.TextField(blank=True)
    city = models.TextField()
    cuisine  = models.TextField(blank=True)
    opening_hours = models.TextField(blank=True)
    #english_friendly = models.BooleanField(blank=True)
    outdoor_seating = models.BooleanField(blank=True)
    website = models.TextField(blank=True)
    # link to menu in static folder
    #menu = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    #osm_id
    way = models.PointField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'planet_osm_point'

# class acceptable_times(models.Model):
#    acceptable_time = models.DateTimeField()
#
#    def __str__(self):
#        return self.acceptable_time

class reservation(models.Model):
    requested_by_user = models.TextField()
    name_reservation = models.TextField()
    name_restaurant = models.TextField()
    party_size  = models.IntegerField()
    time = models.TimeField()
    phone = models.TextField(default='')
    date = models.DateField(default=now)
    caller = models.TextField(blank=True)
    request_completed = models.BooleanField()
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acceptable_time = models.DateTimeField(blank=True, null=True)
    accepted_time = models.DateTimeField(blank=True, null=True)

    # manytomany migration not working https://code.djangoproject.com/ticket/25012?
    # acceptable_times = models.ManyToManyField(acceptable_times)


    def __str__(self):
        return self.name_reservation+''+self.name_restaurant

    class Meta:
        permissions=(
        ('can_accept_calls', 'can accept calls'),
        )


class place_staging(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField()
    requested_by_user = models.TextField(default='anon')
    #name_en = models.TextField(blank=True)
    #city = models.TextField(blank=True)
    #cuisine  = models.TextField(blank=True)
    #opening_hours = models.TextField(blank=True)
    #english_friendly = models.BooleanField(blank=True)
    #outdoor_seating = models.BooleanField(blank=True)
    #website = models.TextField(blank=True)
    # link to menu in static folder
    #menu = models.TextField(blank=True)
    phone = models.TextField()
    #osm_id
    way = models.PointField()

    def __str__(self):
        return self.name

#class myUser(AbstractUser):
#    name_first = models.TextField()
#    name_last = models.TextField()
#    caller = models.BooleanField(blank=True)
