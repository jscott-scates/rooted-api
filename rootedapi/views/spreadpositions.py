from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rootedapi.models import SpreadPosition

class SpreadPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpreadPosition
        fields = (
            "id",
            "spread",
            "position",
            "label",
            "prompt"
        )

