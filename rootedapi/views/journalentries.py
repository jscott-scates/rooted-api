from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rootedapi.models import JournalEntry, Sage, Spread, SpreadPosition, EntryCard
from .sages import SageSerializer
from .spreads import SpreadDetailsSerializer

class JournalEntrySerializer(serializers.ModelSerializer):

    sage = SageSerializer(many=False)
    spread = serializers.SerializerMethodField   

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
            'spread'
        )
        depth = 1

    def get_spread(self, obj):
        spread = obj.spread

        return SpreadDetailsSerializer(spread, context = self.context)

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
            entry.delete()

            return Response({}, status = status.HTTP_204_NO_CONTENT)
        except JournalEntry.DoesNotExist as ex:
            return Response ({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        try:
            #Get the current sage
            sage = Sage.objects.get(user=request.auth.user)

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

            #Create empty entry cards for each spread position
            for position in spread_positions:
                EntryCard.objects.create(
                    journalEntry = new_journal,
                    spread_position = position,
                    card = None #Placeholder value for the cards that will be drawn in the next user action, instantiating as part of journal creation.
                )
            
            #Return the new journal entry
            serializer = JournalEntrySerializer(new_journal, context={"request":request})
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Sage.DoesNotExist:
        
            return Response({"error": "Sage not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"message":ex.args[0]},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        