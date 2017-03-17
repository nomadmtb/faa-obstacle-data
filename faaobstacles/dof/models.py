from django.db import models
from django.contrib.gis.db import models as geo_models

# This model will represent an Obstacle object identified by the FAA.
class Obstacle(models.Model):

    LIGHTING_CHOICES = (
        ('R', 'Red'),
        ('D', 'Medium intensity White Strobe & Red'),
        ('H', 'High intensity White Strobe & Red'),
        ('M', 'Medium intensity White Strobe'),
        ('S', 'High intensity White Strobe'),
        ('F', 'Flood'),
        ('C', 'Duel Medium Catenary'),
        ('W', 'Synchronized Red Lighting'),
        ('L', 'Lighted (Type Unknown)'),
        ('N', 'None'),
        ('U', 'Unknown'),
    )

    ACTION_CHOICES = (
        ('A', 'Add'),
        ('C', 'Change'),
        ('D', 'Dismantle'),
    )

    MARK_INDICATOR_CHOICES = (
        ('P', 'Orange or Orange and White Paint'),
        ('W', 'White Paint Only'),
        ('M', 'Marked'),
        ('F', 'Flag Marker'),
        ('S', 'Spherical Marker'),
        ('N', 'None'),
        ('U', 'Unknown'),
    )

    id = models.IntegerField(primary_key=True, db_index=True)
    country = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    location = geo_models.PointField(null=True)
    type_desc = models.CharField(max_length=25)
    quantity = models.IntegerField()
    agl_height = models.IntegerField()
    amsl_height = models.IntegerField()
    lighting = models.CharField(max_length=1, choices=LIGHTING_CHOICES)
    horizontal_accuracy = models.FloatField(null=True)
    vertical_accuracy = models.FloatField(null=True)
    mark_indicator = models.CharField(max_length=1, choices=MARK_INDICATOR_CHOICES)
    faa_study_id = models.CharField(max_length=250, null=True)
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    action_date = models.DateField()

    def __repr__(self):
        return "<Obstacle:id={0},country={1},lat={2},long={3}...>".format(
            self.id, self.country, self.lat, self.long
        )

# This model will represent an Airport that we will use to build routes etc.
class Airport(models.Model):

    name = models.CharField(max_length=250)
    city = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=250, null=True)
    iata = models.CharField(max_length=3, null=True, db_index=True)
    icao = models.CharField(max_length=4, null=True, db_index=True)
    location = geo_models.PointField(null=True)
    altitude = models.IntegerField()

    def __repr__(self):
        return "<Airport:id={0},icao={1},iata={2}...>".format(
            self.id, self.icao, self.iata
        )
