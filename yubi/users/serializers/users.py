"""Users serializers"""

# Django REST
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator



#Django
from django.contrib.auth import authenticate
from yubi.users import models #metodo para validar los datos
from django.core.validators     import RegexValidator
from django.contrib.auth import password_validation

#Models
from yubi.users.models import User, Profile


#creo modelo para traer los datos desde el modelo
class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'email'
        )

class UserLoginSerializers(serializers.Serializer):
    """ User login serializer
    
    Handle the login request data
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password']) #verifico si existe usuario y si los datos son correctos
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.is_verified: #si no esta verificado no se puede loguear
            raise serializers.ValidationError('Account is not active yet')
        self.context['user'] = user #aca tomamos la instanacia del user para luego poder mostrar los datos
        return data



    # a continuacion, no es lo mas seguro pero a modo ejemplo se utilizaran el authtoken
    # ya que los token son fijos y quedan en la base de datos como texto plano, no van actualizandose
    def create(self, data):
        """Generate  or retrieve new token"""

        token, created = Token.objects.get_or_create(user=self.context['user']) #busco o creo un token
        return self.context['user'], token.key #devolvemos la key del token


#Se puede usar el modelserializer, pero al quere validar la pass lo hacemos manual, a modo ejemplo
class UserSignUpSerializers(serializers.Serializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone numbrer must be entered in the format: +9999999999. Up to 15 digits allowed"
    )

    phone_number = serializers.IntegerField(validators=[phone_regex])

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)


    def validate(self, data):
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise serializers.ValidationError("Password don't match")            
        
        password_validation.validate_password(password) #verifica la password, validador de django default(como cuando creamos superuser django)

        return data
    
    def create(self, data):
        data.pop('password_confirmation')#sacamos del data para que no se guarde al crear el objecto
        user = User.objects.create_user(**data) #creador del manager de user
        profile = Profile.objects.create(user=user)
        return user



