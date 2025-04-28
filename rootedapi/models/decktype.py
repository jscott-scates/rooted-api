from django.db import models

class DeckType(models.Model):
    name = models.CharField(max_length=55)
    label = models.CharField(max_length=55)
    description = models.CharField(max_length=250)
    