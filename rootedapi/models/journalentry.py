from django.db import models
from .sage import Sage

class Mood(models.TextChoices):
    #Mood = value , label
    CALM = 'calm', 'Calm'
    HOPEFUL = 'hopeful', 'Hopeful'
    REFLECTIVE = 'reflective', 'Reflective'
    JOYFUL = 'joyful', 'Joyful'
    GRATEFUL = 'grateful', 'Grateful'
    PEACEFUL = 'peaceful', 'Peaceful'
    CURIOUS = 'curious', 'Curious'
    EMPOWERED = 'empowered', 'Empowered'
    GROUNDED = 'grounded', 'Grounded'
    ANXIOUS = 'anxious', 'Anxious'
    MELANCHOLY = 'melancholy', 'Melancholy'
    FRUSTRATED = 'frustrated', 'Frustrated'
    OVERWHELMED = 'overwhelmed', 'Overwhelmed'
    LONELY = 'lonely', 'Lonely'
    GRIEVING = 'grieving', 'Grieving'
    VULNERABLE = 'vulnerable', 'Vulnerable'
    LOST = 'lost', 'Lost'
    INSPIRED = 'inspired', 'Inspired'
    MOTIVATED = 'motivated', 'Motivated'
    DETERMINED = 'determined', 'Determined'
    REJUVENATED = 'rejuvenated', 'Rejuvenated'

class LunarPhase(models.TextChoices):
    #LunarPhase = value, label
    NEW_MOON = 'New Moon', '🌑'
    WAXING = 'Waxing Moon', '🌔'
    FULL_MOON = 'Full Moon', '🌕'
    WANING = 'Waning Moon', '🌖'

class JournalEntry(models.Model):
    sage = models.ForeignKey(Sage, on_delete=models.CASCADE, related_name="journal")
    initial_seed = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    entry_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    mood = models.CharField(
        max_length=25,
        choices=Mood.choices,
        null=True,
        blank=True
    )
    lunar_phase = models.CharField(
        max_length=25,
        choices=LunarPhase.choices,
        null=True,
        blank=True
    )
    spread = models.ForeignKey("Spread", on_delete=models.CASCADE, related_name="journal_spread")
