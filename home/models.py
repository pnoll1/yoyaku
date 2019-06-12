from django.contrib.gis.db import models
from django.utils.timezone import now
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
    city = models.TextField()
    way = models.PointField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'home_planet_osm_point'


class reservation(models.Model):
    requested_by_user = models.TextField()
    name_reservation = models.TextField()
    name_restaurant = models.TextField()
    party_size  = models.IntegerField()
    time = models.TimeField()
    date = models.DateField(default=now)
    caller = models.TextField(blank=True)
    request_completed = models.BooleanField()
    # restaurant uuid should be tied to res as well

    def __str__(self):
        return self.name_reservation+''+self.name_restaurant
