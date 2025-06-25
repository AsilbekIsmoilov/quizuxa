from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    is_intern = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
