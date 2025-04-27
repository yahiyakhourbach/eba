from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    first_name          = models.CharField(max_length=255, null=False)
    last_name           = models.CharField(max_length=255, null=False)
    email               = models.EmailField(max_length=255, null=False, unique=True)
    is_moderator        = models.BooleanField(default=False)

    REQUIRED_FIELDS     = ['email','first_name','last_name']

    def __str__(self):
        return f'{self.username}'

