from django.db import models

# Create your models here.
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

    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    lat = models.FloatField()
    long = models.FloatField()
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


class Airport(models.Model):

    name = models.CharField(max_length=250)
    city = models.CharField(max_length=250, null=True)
    country = models.CharField(max_length=250, null=True)
    iata = models.CharField(max_length=3, null=True)
    icao = models.CharField(max_length=4, null=True)
    lat = models.FloatField()
    long = models.FloatField()
    altitude = models.IntegerField()
