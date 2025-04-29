from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rootedapi.models import Spread, SpreadPosition

#SpreadPositionSerializer serializes the positions associated to a pk of a spread
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

#SpreadSerializer is used to get a baseline of data for the ViewSet list function
class SpreadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spread
        fields = (
            "id",
            "name",
            "description",
            "num_positions",
        )

#SpreadDetailsSerializer returns the spread details and the related SpreadPositions
class SpreadDetailsSerializer(serializers.ModelSerializer):
    spread_positions = serializers.SerializerMethodField()

    class Meta(SpreadSerializer.Meta):
        fields = SpreadSerializer.Meta.fields+("spread_positions",)
    
    def get_spread_positions(self, obj):
        positions = SpreadPosition.objects.filter(spread=obj.pk)
        return SpreadPositionSerializer(positions, many=True, context=self.context).data


#Spread ViewSet does not include Create and Destroy as Users do not have permissions to create and destroy Spreads.
class Spreads(ViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        spreads = Spread.objects.all()
        serializer = SpreadSerializer(spreads, many=True, context={"request": request})

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            spread = Spread.objects.get(pk=pk)
            serializer = SpreadDetailsSerializer(spread, many=False, context={"request":request})
            return Response(serializer.data)
        except Spread.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        