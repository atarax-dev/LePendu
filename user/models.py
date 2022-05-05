from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    played_games = models.IntegerField(default=0)
    won_games = models.IntegerField(default=0)
    rank = models.IntegerField(null=True)
    streak = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username}"


class Badges(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
