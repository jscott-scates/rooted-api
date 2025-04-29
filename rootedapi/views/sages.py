from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rootedapi.models import Sage, Deck


class SageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sage
        url = serializers.HyperlinkedIdentityField(
            view_name='sage',
            lookup_field='id'
        )
        fields =('id','user','deck')

class Sages(ViewSet):
    
    def update(self, request, pk=None):
        sage = Sage.objects.get(user = request.auth.user)
        sage.user.last_name = request.data["last_name"]
        sage.user.email = request.data["email"]
        sage.deck = Deck.objects.get(pk=request.data["deck"])
        sage.user.save()
        sage.save()

        return Response({},status = status.HTTP_204_NO_CONTENT)
