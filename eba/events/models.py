from django.db import models
from django.contrib.gis.db import models as geomodels
from users.models import User
# Create your models here.

class Event(models.Model):

    user            = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    title           = models.CharField(max_length=255,null=False)
    description     = models.TextField(null=False)
    date            = models.DateTimeField()
    location        = geomodels.PointField()
    nbr_reserved    = models.IntegerField(default=0)
    capacity        = models.IntegerField(default=0)