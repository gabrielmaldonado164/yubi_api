"""Users views"""

#Django REST Framework
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response    import Response
from rest_framework import status



#Serializer
from yubi.users.serializers.users import (UserLoginSerializers, UserModelSerializer, UserSignUpSerializers)

class UserLoginAPIView(APIView):
    """User login API view"""
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request"""
        serializers = UserLoginSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        user, token = serializers.save()
        data = { #mala practica, solo de ejemplo este dic de data
            'user':UserModelSerializer(user).data, #muestro los datos del user
            'access_token':token 
        }

        return Response(data, status=status.HTTP_201_CREATED)



class UserSignUpAPIView(APIView):
    """User signup API view"""
    def post(self, request, *args, **kwargs):
        """Handle HTTP POST request"""
        serializers = UserSignUpSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save() #esto va de la mano del create
        data = UserModelSerializer(user).data

        return Response(data, status=status.HTTP_201_CREATED)
