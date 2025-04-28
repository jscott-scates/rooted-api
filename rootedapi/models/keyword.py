from django.db import models

class Keyword(models.Model):
    name = models.CharField(max_length=55)
    label = models.CharField(max_length=55)
    