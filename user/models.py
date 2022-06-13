from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    played_games = models.IntegerField(default=0)
    won_games = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)

    @property
    def win_rate(self):
        try:
            win_rate = self.won_games / self.played_games
            return int((round(win_rate, 2))*100)
        except ZeroDivisionError:
            return 0

    @property
    def rank(self):
        players = User.objects.all()
        sorted_players = sorted(players, key=lambda player: player.win_rate, reverse=True)
        for sorted_player in sorted_players:
            if sorted_player.username == self.username:
                if self.username == "superadmin":
                    return 0
                rank = sorted_players.index(sorted_player) + 1
                break
        return rank

    def __str__(self):
        return f"{self.username}"


class Badge(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
