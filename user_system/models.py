import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    create_date = models.DateTimeField(default=None,null=True)
    on_date = models.DateTimeField(default=None,null=True)

class UserVerification(models.Model):
    email = models.CharField(max_length=20,default='')
    token = models.CharField(max_length=200)
    otp = models.CharField(max_length=6,default='')
    isVerified = models.BooleanField(default=False)
