from django.db import models
from .card import Card
from .keyword import Keyword

class CardKeyword(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    