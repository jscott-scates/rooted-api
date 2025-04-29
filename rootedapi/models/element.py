from django.db import models

class Element(models.Model):
    name = models.CharField(max_length=20)
    label = models.CharField(max_length=20)
    icon = models.CharField(max_length=1)
    