from django.db import models
from django.contrib.auth.models import User

class Sage(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    deck = models.ForeignKey("Deck", on_delete=models.DO_NOTHING, related_name="preferred_deck")
    