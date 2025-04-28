from django.db import models

class Spread(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    num_positions = models.IntegerField()
    
