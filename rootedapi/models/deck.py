from django.db import models
from .decktype import DeckType

class Deck(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=700)
    theme = models.CharField(max_length=55)
    deck_type = models.ForeignKey(DeckType, on_delete=models.DO_NOTHING, related_name="decks")
