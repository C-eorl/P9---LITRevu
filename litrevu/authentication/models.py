from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Custom User Model """
    profile_picture = models.ImageField(upload_to="avatars/", null=True, blank=True)
