from django.db import models
from .spread import Spread

class SpreadPosition(models.Model):
    spread = models.ForeignKey(Spread, on_delete=models.CASCADE, related_name="positions")
    position = models.IntegerField()
    label = models.CharField(max_length=50)
    prompt = models.CharField(max_length=150)
