from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rootedapi.models import Element

class ElementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Element
        url = serializers.HyperlinkedIdentityField(
            view_name = 'element',
            lookup_field='id'
        )
        fields = (
            'id',
            'name',
            'label',
            'icon'
        )

class Elements(ViewSet):

    def list(self, request):
        elements = Element.objects.all()
        serializer = ElementSerializer(elements, many=True, context={"request":request})

        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            element = Element.objects.get(pk=pk)
            serializer = ElementSerializer(element, many=False, context={"request":request})

            return Response(serializer.data)
        except Element.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 