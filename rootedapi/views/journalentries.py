import random
from django.http import HttpResponseServerError, HttpResponseForbidden
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rootedapi.models import JournalEntry, Sage, SpreadPosition, EntryCard, Card
from .sages import SageSerializer
from .spreads import SpreadDetailsSerializer
from .entrycards import EntryCardSerializer

class JournalEntrySerializer(serializers.ModelSerializer):

    sage = SageSerializer(many=False, read_only=True)
    spread = serializers.SerializerMethodField(read_only=True)
    entry_cards = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = JournalEntry
        fields = (
            'id',
            'sage',
            'initial_seed',
            'title',
            'entry_text',
            'created_on',
            'mood',
            'lunar_phase',
            'spread',
            'entry_cards'
        )
        depth = 1

    def get_spread(self, obj):
        spread = obj.spread

        return SpreadDetailsSerializer(spread, context = self.context).data
    
    def get_entry_cards(self,obj):
        entry_card = obj.entry_cards.all()

        return EntryCardSerializer(entry_card, many=True, context=self.context).data

class JournalEntries(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    def list(self, request):
        current_sage = Sage.objects.get(user=request.auth.user)
        entries = JournalEntry.objects.filter(sage = current_sage)
        serializer = JournalEntrySerializer(entries, many=True, context={"request": request})

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            current_sage = Sage.objects.get(user=request.auth.user)
            entry = JournalEntry.objects.get( pk = pk, sage = current_sage)
            serializer = JournalEntrySerializer(entry, many=False, context={"request":request})

            return Response(serializer.data)
        
        except Exception as ex:
            
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        try:
            current_sage = Sage.objects.get(user=request.auth.user)
            entry = JournalEntry.objects.get(pk=pk,sage = current_sage)
            entry_cards = EntryCard.objects.filter(journalEntry=pk)

            for card in entry_cards:
                card.delete()

            entry.delete()

            return Response({}, status = status.HTTP_204_NO_CONTENT)
        except JournalEntry.DoesNotExist as ex:
            return Response ({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        try:
            #Get the current sage
            sage = Sage.objects.get(user=request.auth.user)

            #Get list of all cards that belong to sage's preferred deck
            deck_cards = list(Card.objects.filter(deck=sage.deck))

            #Shuffle the Cards to ensure they are in a random order (non-destructive)
            random.shuffle(deck_cards)

            #Get the spread id from the request
            spread_id = request.data.get("spread")
            if not spread_id:
                return Response({"error": "Spread ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            #Create an empty journal entry
            new_journal = JournalEntry.objects.create(
                sage = sage,
                spread_id = spread_id,
                initial_seed = None,
                title = "",
                mood = None,
                lunar_phase= None
            )
            
            #Fetch all positions tied to the selected spread
            spread_positions = SpreadPosition.objects.filter(spread_id = spread_id)

            #Create entry cards for each spread position and assign a unique card to each position
            #Using the i allows us to index the cards in teh deck and ensure that we do not draw the same card in a single spread
            for i, position in enumerate(spread_positions):
                if i < len(deck_cards):
                    EntryCard.objects.create(
                        journalEntry = new_journal,
                        spread_position = position,
                        card = deck_cards[i]
                    )
                else:
                    # Handle edge case where not enough cards exist
                    EntryCard.objects.create(
                        journalEntry=new_journal,
                        spread_position=position,
                        card=None
                    )
            
            #Return the new journal entry
            serializer = JournalEntrySerializer(new_journal, context={"request":request})
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Sage.DoesNotExist:
        
            return Response({"error": "Sage not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"message":ex.args[0]},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, pk=None):

        try: 
            current_sage = Sage.objects.get(user = request.auth.user)
            entry = JournalEntry.objects.get(pk=pk)

            if entry.sage != current_sage:
                return HttpResponseForbidden("You do not have permission to update this journal entry.")
            
            entry.initial_seed = request.data.get("initial_seed", entry.initial_seed)
            entry.title = request.data.get("title", entry.title)
            entry.entry_text = request.data.get("entry_text",entry.entry_text)
            entry.mood = request.data.get("mood", entry.mood)
            entry.lunar_phase = request.data.get("lunar_phase", entry.lunar_phase)
            entry.created_on = entry.created_on
            entry.sage = entry.sage
            entry.spread = entry.spread

            entry.save()

            return Response({},status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:

            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
