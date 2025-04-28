from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User

#Serializers
class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model=User
        url = serializers.HyperlinkedIdentityField(
            view_name='user',
            lookup_field = 'id'
        )
        fields = ('id','url','username','password','first_name','last_name','email','date_joined')

#ViewSet
class Users(ViewSet):
    def retrieve(self, request, pk=None):
        """Handle GET requests for single user/sage"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={'request':request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self,request):
        """Handle GET requests for all users in the database"""
        users = User.objects.all()
        serializer = UserSerializer(
            users, many=True, context={'request':request}
        )
        return Response(serializer.data)