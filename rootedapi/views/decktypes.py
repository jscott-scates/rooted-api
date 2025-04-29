from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rootedapi.models import DeckType

class DeckTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeckType
        fields = (
            'id',
            'name',
            'label',
            'description',
        )