"""Users serializers"""

# Django REST
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator



#Django
from django.contrib.auth        import authenticate #metodo para validar los datos
from yubi.users                 import models 
from django.core.validators     import RegexValidator
from django.contrib.auth        import password_validation
from django.core.mail           import EmailMultiAlternatives
from django.template.loader     import render_to_string
from django.utils               import timezone
from django.conf                import settings

#Models
from yubi.users.models import User, Profile

#Utilities
import jwt

#Python
from datetime import timedelta

#creo modelo para traer los datos desde el modelo (list)
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
        self.context['user'] = user #aca tomamos la instanacia del user para luego poder mostrar los datos en el create
        return data

    # a continuacion, no es lo mas seguro pero a modo ejemplo se utilizaran el authtoken
    # ya que los token son fijos y quedan en la base de #metodo para validar los datosmos la key del token
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
        profile = Profile.objects.create(user=user) #creo que el profile
        self.send_confirmation_email(user) #metodo para el envio de confirmacion de cuenta, como solo lo utilizo por el momento para esta funcioncalida de crear usuarios, lo genero como metodo de este serializer
        return user


    def send_confirmation_email(self, user): #lo envia por consola en local
        """Send account verification link to given user"""
        verification_token = self.gen_verification_token(user) #nos regresa un token de usario para el email
        subject  = 'Welcome@{}! Verify your account to start using Comparte Ride'
        from_email = 'yubi <noreply@yubi.com>'
        content = render_to_string('emails/users/account_verified.html', {
            'token':verification_token,
            'user' :user
        })
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """Create JWT token that the user can user to verify its account"""
        exp_date = timezone.now() + timedelta(days=3) # time delta es para la diferencia entre fechas y horas 
        payload = {
            'user':user.username,
            'exp':int(exp_date.timestamp()),#es el UNIX TIME en milisegundos -- 'exp' es propieda de jwt para la expiracion de TOKENs
            'type':'email_confirmation' #tipo de token que generamos
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256') #generamor el encode r

        return token


class AccountVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, data):
        "Verify token is valid"

        try:#decodeamos el token 
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
        
        self.context['payload'] = payload
        return data
    
    def save(self):
        """Update user's verified status"""

        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()