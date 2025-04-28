from django.db import models
from .deck import Deck

class Card(models.Model):
    name = models.CharField(max_length=55)
    meaning = models.CharField(max_length=1500)
    orientation_enabled = models.BooleanField(default=False)
    image_path = models.ImageField(
        upload_to="cards",
        null=True
    )
    element = models.ForeignKey("Element", on_delete=models.PROTECT, related_name="card_element")
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card_type = models.ForeignKey("CardType", on_delete=models.PROTECT)
    keywords = models.ManyToManyField("Keyword", through="CardKeyword", related_name="keyword_cards")
