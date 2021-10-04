"""Users models"""
# Python
from __future__                 import unicode_literals

#Django
from django.db import models
from django.utils.translation   import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.validators     import RegexValidator
from django.core                import validators


# Utilities
from yubi.utils.models import YubiModels

class User(YubiModels, AbstractUser):
    """Users model
    Extend from Django Abstract User, change the username field
    to email and add some extra field
    """

    email = models.EmailField(verbose_name=_(u'Email addres'), 
        unique=True, 
        error_messages={
            'unique':'A user with that email alredy exists'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone numbrer must be entered in the format: +9999999999. Up to 15 digits allowed"
    )
    phone_number = models.CharField(verbose_name=_(u'Numero telefonico'),validators=[phone_regex], max_length=17, blank=True)

    USERNAME_FIELD = 'email' #cambio el username por email para loguear
    REQUIRED_FIELDS= ['username', 'first_name', 'last_name']

    is_client  = models.BooleanField(
        verbose_name=_(u'Estado Cliente'),
        default=False,
        help_text=(
            'Help easily disinguish users and perform queries.'
            'Clients are the main type of user'
        )
    )

    is_verified = models.BooleanField(
        verbose_name=_(u'Verificacion de email'),
        default=False,
        help_text='Set to true when the user have verified its email addres.'
    )

    def __str__(self):
        return  self.username
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.username
