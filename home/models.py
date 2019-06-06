from django.contrib.gis.db import models

class place(models.Model):
    name = models.TextField()
    name_en = models.TextField(blank=True)
    city = models.TextField()
    cuisine  = models.TextField(blank=True)
    hours = models.TextField(blank=True)
    english_friendly = models.BooleanField(blank=True)
    outdoor_seating = models.BooleanField(blank=True)
    website = models.TextField(blank=True)
    # link to menu in static folder
    menu = models.TextField(blank=True)
    lon = models.FloatField()
    lat = models.FloatField()

    def __str__(self):
        return self.name
# planet_osm_point table for tags osm_id first Col
# planet_osm_nodes table with id, lat ,long

class planet_osm_point(models.Model):
    name = models.TextField()
    name_en = models.TextField(blank=True)
    cuisine  = models.TextField(blank=True)
    opening_hours = models.TextField(blank=True)
    #english_friendly = models.BooleanField(blank=True)
    outdoor_seating = models.BooleanField(blank=True)
    website = models.TextField(blank=True)
    #phone = models.TextField(blank=True)
    # uuid =models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #osm_id
    city = models.TextField()
    way = models.PointField()
    geom = models.PointField()
    def __str__(self):
        return self.name

class reservation(models.Model):
    requested_by_user = models.TextField()
    name_reservation = models.TextField()
    name_restaurant = models.TextField()
    party_size  = models.IntegerField()
    time = models.TimeField()
    caller = models.TextField()
    request_completed = models.BooleanField()


    def __str__(self):
        return self.name_reservation
