"""Boxes models"""
# Python
from __future__                 import unicode_literals

#Django
from django.db                  import models
from django.utils.translation   import ugettext_lazy as _


# Utilities
from yubi.utils.models import YubiModels

class Box(YubiModels):
    name = models.CharField(verbose_name=_(u'Nombre'), max_length=144)
    slug_name = models.SlugField(verbose_name=_(u'Slug field'), unique=True, max_length=40)

    about = models.CharField(verbose_name=_(u'Descripcion'), max_length=255, blank=True)
    picture = models.ImageField(verbose_name=_(u'Imagen'), 
        upload_to='boxes/pictures', 
        blank=True, 
        null=True 
    )

    #Stats
    rides_offered = models.PositiveIntegerField(verbose_name=_(u'Viajes ofrecidos'), default=0)
    rides_taken = models.PositiveIntegerField(verbose_name=_(u'Viajes tomados'), default=0)

    is_verified = models.BooleanField(verbose_name=_(u'Verificador'),
        default=False, 
        help_text='Verified if is official communites'
    )

    is_public = models.BooleanField(verbose_name=_(u'Publico'), 
        default=True,
        help_text='If is public or private'
    )

    is_limited = models.BooleanField(verbose_name=_(u'Limites de miembros'),default=False)
    member_limited = models.PositiveIntegerField(verbose_name=_(u'Cantidad del limite'), default=0)


    def __str__(self):
        """Return box name"""
        return self.name


    class Meta(YubiModels.Meta):
        ordering = ['-rides_taken','-rides_offered']
        
    