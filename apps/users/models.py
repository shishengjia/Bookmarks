from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return '{}'.format(self.username)
