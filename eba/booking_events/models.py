from django.db import models
from django.contrib.gis.db import models as geomodels

# Create your models here.

class Event(models.Model):

    title       = models.CharField(max_length=255,null=False)
    description = models.TextField(null=False)
    date        =  models.DateTimeField()
    location    = geomodels.PointField()
    capacity    = models.IntegerField()