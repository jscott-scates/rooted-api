from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rootedapi.models import Deck
from .decktypes import DeckTypeSerializer

class DeckSerializer(serializers.HyperlinkedModelSerializer):
    deck_type_info = serializers.SerializerMethodField()

    class Meta:
        model = Deck
        fields = (
            'id',
            'name',
            'description',
            'theme',  
            'deck_type_info'
        )
    
    def get_deck_type_info(self, obj):
        type_of_deck = obj.deck_type

        return DeckTypeSerializer(type_of_deck, context=self.context).data

#Users can not create or destroy existing decks, this is reflected in the ViewSet   
class Decks(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        decks = Deck.objects.all()
        serializer = DeckSerializer(decks, many=True, context={"request":request})
        
        return Response(serializer.data)
   
    def retrieve(self, request, pk=None):
        try:
            deck = Deck.objects.get(pk=pk)
            serializer = DeckSerializer(deck, many=False, context={"request": request})

            return Response(serializer.data)
        except Deck.DoesNotExist as ex:

            return Response({"message": ex.args[0]},status=status.HTTP_404_NOT_FOUND)
 