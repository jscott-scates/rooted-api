import datetime
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rootedapi.models import Sage
from .users import UserSerializer
from .sages import SageSerializer

class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=False)

    class Meta:
        model = Sage
        fields = (
            'id',
            'user',
            'deck'
        )
        depth = 1

class Profile(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self,request):
        try:
            current_user = Sage.objects.get(user=request.auth.user)
            serializer = ProfileSerializer(
                current_user, many=False, context={"request":request}
            )
            
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)