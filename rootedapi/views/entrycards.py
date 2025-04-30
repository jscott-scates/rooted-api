from django.http import HttpResponseServerError, HttpResponseForbidden
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rootedapi.models import Sage, Card, JournalEntry, SpreadPosition, EntryCard
from .cards import CardSerializer
from .spreads import SpreadPositionSerializer

class EntryCardSerializer(serializers.ModelSerializer):
    #spreadposition
    card = serializers.SerializerMethodField
    spread_position = serializers.SerializerMethodField

    class Meta:
        model = EntryCard
        fields = (
            'id',
            'card',
            'spread_position'
        ) #do not need journal entry as that is passed in by the query params
        depth=1
    
    def get_card(self, obj):
        card = obj.card

        return CardSerializer(card, context = self.context)
    
    def get_spread_position(self, obj):
        position = obj.spread_position

        return SpreadPositionSerializer(position, context = self.context)
    
class EntryCards(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        current_sage = Sage.objects.get(user = request.auth.user)
        journal_entry_id = request.query_params.get('journal-entry')
        
        if not journal_entry_id:
            
            return Response({"message": "Missing the journal-entry query parameter."})
        
        try:
            journal_entry = JournalEntry.objects.get(pk=journal_entry_id,sage=current_sage)
            cards = EntryCard.objects.filter(journalEntry = journal_entry)
            serializer = EntryCardSerializer(cards, many=True, context={"request":request})

            return Response(serializer.data)
        
        except JournalEntry.DoesNotExist:
            return Response({'message': "Journal entry not found or does not belong to current user."})
    
    def update(self, request, pk=None):
        try:
            current_sage = Sage.objects.get(user = request.auth.user)
            entry_card = EntryCard.objects.get(pk=pk)

            if entry_card.journalEntry.sage != current_sage:
                return HttpResponseForbidden("You do not have permission to update this entry card.")
            
            card_id = request.data.get("card")
            entry_card.card = Card.objects.get(pk=card_id)
            entry_card.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            
            return Response({"message":ex.args[0]},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        