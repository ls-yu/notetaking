from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

class User(AbstractUser):
    is_notetaker = models.BooleanField(default=False)
    is_noterequester = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    school_code = models.CharField(max_length=6)