from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    '''Extends Django.contrib.auth.models. User is one-to-one relation. is_active is True by default (set to false if logged out, or they turn it off).'''
    user = models.OneToOneField( User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class GameRoom(models.Model):
    '''Potentially use a model to store all logged in Users for Viewing? Or can I get access to ALL User.objects in a view??'''
    pass