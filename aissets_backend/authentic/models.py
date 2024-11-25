from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    points = models.IntegerField(default=0)  # Points for gamification
    badges = models.ManyToManyField('Badge', blank=True, related_name='users')  # Badges earned

    def __str__(self):
        return self.username

class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='badges/', blank=True, null=True)
    points_required = models.IntegerField()

    def __str__(self):
        return self.name

class Leaderboard(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='leaderboard')
    rank = models.IntegerField()

    def __str__(self):
        return f"Rank {self.rank} - {self.user.username}"
