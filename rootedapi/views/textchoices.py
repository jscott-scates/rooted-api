from rest_framework.decorators import api_view
from rest_framework.response import Response
from rootedapi.models import JournalEntry

#api_view turns a function into an API view, can be used on models.TextChoices to get list of choices returned to front end
@api_view(['GET'])
def get_journal_choices(request):
    mood_choices = [
        {"value": value, "label":label}
        for value, label in JournalEntry._meta.get_field('mood').choices
    ]
    lunar_choices = [
        {"value": value, "label": label}
        for value, label in JournalEntry._meta.get_field('lunar_phase').choices
    ]
    return Response({
        "moods": mood_choices,
        "lunar_phases": lunar_choices
    })