"""Django models utilities"""
# Python
from __future__                 import unicode_literals


# Django
from django.db                  import models
from django.conf    import settings
from django.utils.translation   import ugettext_lazy as _
from django.contrib.auth.models import User
from crum                       import get_current_user



# The YubiModels class is an abstract base class which is inherited by all models in the project.
# It provides the date_created and date_modified fields, which automatically populate with the current date when the record is created or modified.
# It also provides user_creation and user_update fields, which are automatically populated with the current user when the record is created or modified.
# 
# Args:
#   self: The model instance that is being saved. This is either an existing instance or newly created.
#   *args: Any additional arguments are passed to the superclass.
#   **kwargs: 
# Returns:
#   A dict with the following keys:
#     * success: a boolean indicating if the call was successful or not
#     * value: the value of the field that was requested
#     * error: if an error occurred, a description of the error
class YubiModels(models.Model):
    """Comparte Yubi base models"""

    date_created    = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Fecha de creacion'))
    user_creation   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                        related_name='%(class)s_create_for',
                                        null=True, 
                                        blank=True, 
                                        verbose_name=_(u'Usuario creador')
                                    )

    date_modified   = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Fecha de modificacion'))
    user_update     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                        related_name='%(class)s_update_for',
                                        null=True, 
                                        blank=True, 
                                        verbose_name=_(u'Usuario modificacor')
                                    )
    

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
                self.date_created = self.date_created
            else:
                self.user_update = user
                self.date_modified = self.date_modified

        super(YubiModels, self).save(*args, **kwargs)


    class Meta:
        abstract = True
        get_latest_by = 'date_created'
        ordering = ["-date_created", "-date_modified"]
