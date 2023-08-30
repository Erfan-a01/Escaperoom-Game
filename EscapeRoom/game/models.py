from django.db import models
from accounts.player_models import Player

# Create your models here.


class Room(models.Model):
    title = models.CharField(max_length=100)  # subject of the game
    question_num = models.PositiveIntegerField()  # The question number of the game
    total_score = models.PositiveIntegerField()  # Sum of the scores in the game

    def __str__(self):
        return self.title


class Question(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    score = models.PositiveIntegerField()
    answer = models.CharField(max_length=100)


class Result(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

