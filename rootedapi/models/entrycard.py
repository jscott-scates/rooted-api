from django.db import models
from .journalentry import JournalEntry
from .card import Card
from .spreadposition import SpreadPosition

class EntryCard(models.Model):
    journalEntry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name="entry_cards")
    card = models.ForeignKey(Card, on_delete=models.PROTECT, null=True, blank=True) #Want this to be null when instantiated originally
    spread_position=models.ForeignKey(SpreadPosition, on_delete=models.SET_NULL, null=True)