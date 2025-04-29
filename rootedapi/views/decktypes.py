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

#Only created list function at this time, should not need create or destroy as users don't have the option but may need retrieve.
class DeckTypes(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        decktypes = DeckType.objects.all()
        serializer = DeckTypeSerializer(decktypes, many=True, context={"request": request})

        return Response(serializer.data)