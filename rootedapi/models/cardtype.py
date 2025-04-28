from django.db import models

class CardType(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length = 100)
    description = models.CharField(max_length=250)
