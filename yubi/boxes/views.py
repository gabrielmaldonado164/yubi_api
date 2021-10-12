"""Box views"""

# Django
from django.http import JsonResponse
from rest_framework import serializers

#Django REST
from rest_framework.decorators import api_view
from rest_framework.response    import Response

# custom
from yubi.boxes.models.box import Box

# Serializer
from yubi.boxes.serializers import BoxSerializer, CreateBoxSerializer

@api_view(['GET'])
def list_box(request):

    box = Box.objects.filter(is_public=True) #query
    serializers = BoxSerializer(box, many=True) #paso la query al serializer y le digo que son un dict de datos

    return Response(serializers.data) #muestro los datos con .data



@api_view(['POST'])
def create_box(request):
    serializer = CreateBoxSerializer(data=request.data) #le paso los datos del data
    serializer.is_valid(raise_exception=True) #verifico si los datos son validos, o mando un raise en caso de que no
    data = serializer.data #mostramos los datos 
    box = serializer.save() #guardamos la instancia del create del serializer

    return Response(BoxSerializer(box).data)



""" Mostrar los datos sin serializers 
@api_view(['GET']) 
def list_box(request):
    data = []
    box = Box.objects.filter(is_public=True)
    for i in box:
        data.append({
            'name':i.name,
            'slug_name':i.slug_name,
            'rides_taken':i.rides_taken,
            'rides_offered':i.rides_offered,
            'member_limited':i.member_limited
        })
    
    return Response(data)
 """


""" Crear sin serializers

@api_view(['POST'])
def create_box(request):
    #request.data == request.POST de django
    name = request.data['name']
    slug_name = request.data['slug_name']
    box = Box.objects.create(name=name, slug_name=slug_name)
    data = {
        'name':box.name,
        'slug_name':box.slug_name,
        'rides_taken':box.rides_taken,
        'rides_offered':box.rides_offered,
        'member_limited':box.member_limited
    }

    return Response(data)

 """

"""
Echo sin django rest, el ejemplo es asi:

def list_box(request):

    data = []
    box = Box.objects.filter(is_public=True)

    for i in box:
        data.append({
            'name':i.name,
            'slug_name':i.slug_name,
            'rides_taken':i.rides_taken,
            'rides_offered':i.rides_offered,
            'member_limited':i.member_limited
        })
    


    return JsonResponse(data, safe=False)
"""