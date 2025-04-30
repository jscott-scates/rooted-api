from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rootedapi.models import Element, CardType, Keyword, Card
from .decks import DeckSerializer

#Elements are descriptive tools added to the Card
class ElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Element
        fields = (
            'id',
            'name',
            'label',
            'icon'
        )

#CardType is a descriptive tool added to the card only
class CardTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardType
        fields = (
            'id',
            'name',
            'label',
            'description'
        )

#Keywords are a descriptive tool added to the card only
class KeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = Keyword
        fields = (
            'id',
            'name',
            'label'
        )

class CardSerializer(serializers.HyperlinkedModelSerializer):
    #Figure out how to add URL
    element = serializers.SerializerMethodField()
    deck = serializers.SerializerMethodField()
    card_type = serializers.SerializerMethodField()
    keywords = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'meaning',
            'orientation_enabled',
            'image_path',
            'element',
            'deck',
            "card_type",
            "keywords"
        )
    
    def get_element(self, obj):
        element = obj.element

        return ElementSerializer(element, context=self.context).data

    def get_deck(self, obj):
        deck = obj.deck

        return DeckSerializer(deck, context=self.context).data
    
    def get_card_type(self, obj):
        type_of_card = obj.card_type

        return CardTypeSerializer(type_of_card, context=self.context).data
    
    def get_keywords(self,obj):
        return KeywordSerializer(obj.keywords.all(), many=True).data
    
class Cards(ViewSet):

    def list(self, request):
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True, context={"request":request})

        return Response(serializer.data)
    
    def retrieve(self,request, pk=None):
        try:
            card = Card.objects.get(pk=pk)
            serializer = CardSerializer(card, many=False, context={"request": request})

            return Response(serializer.data)
        except Card.DoesNotExist as ex:

            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)