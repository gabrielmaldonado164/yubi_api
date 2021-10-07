"""Serializers models BOX"""

# Django REST
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


# Custom
from yubi.boxes.models.box import Box


#Aclaracion, esto se puede hacer con ModelSerializer tambien para que lo hago contra el modelo
class BoxSerializer(serializers.Serializer):
    """Box serializer"""

    name = serializers.CharField()
    slug_name  = serializers.SlugField()
    rides_taken = serializers.IntegerField() 
    rides_offered = serializers.IntegerField() 
    member_limited = serializers.IntegerField() 


class CreateBoxSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=144)
    slug_name = serializers.SlugField(max_length=40,
        validators=[UniqueValidator(queryset=Box.objects.all())] #valida que sea unico en el modelo con el query(query obligatorio)
    )

    about = serializers.CharField(max_length=255, required=False)

    def create(self, data):
        return Box.objects.create(**data)
