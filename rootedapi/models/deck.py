from django.db import models

class Deck(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=700)
    theme = models.CharField(max_length=55)
    deck_type = models.ForeignKey("DeckType", on_delete=models.SET_NULL, related_name="deck_type")
