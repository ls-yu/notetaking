from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

class User(AbstractUser):
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    is_notetaker = models.BooleanField(default=False)
    is_noterequester = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    school_code = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user

class Class(models.Model):
    class_code = models.CharField(max_length=6)
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="classes_teaching")
    students = models.ManyToManyField(UserProfile, related_name="classes_taking", symmetrical=False)

    def __str__(self):
        return self.name


class Note(models.Model):
    which_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(max_length=100)
    #image = models.ImageField(upload_to='images', blank=True)
    text = models.CharField(max_length=15000)
    notetaker = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="notes")
    date = models.CharField(max_length=10)
    note_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.which_class.name + " note by " + self.notetaker
