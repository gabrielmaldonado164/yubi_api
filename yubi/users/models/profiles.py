"""Profile models"""
# Python
from __future__                 import unicode_literals

#Django
from django.db import models
from django.utils.translation   import ugettext_lazy as _


# Utilities
from yubi.utils.models import YubiModels

class Profile(YubiModels):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    picture = models.ImageField(
        verbose_name=_(u'Imagen'),
        upload_to='users/pictures/',
        blank=True,
        null=True
    )

    biography = models.TextField(verbose_name=_(u'Biografia'), max_length=500, blank=True)

    #Stats
    rides_taken = models.PositiveBigIntegerField(verbose_name=_(u'Viajes tomados'), default=0)
    rides_offered = models.PositiveBigIntegerField(verbose_name=_(u'Viajes ofrecidos'), default=0)
    reputation = models.FloatField(verbose_name=_(u'Reputacion'), default=0.0)

    def __str__(self):
        return str(self.user)