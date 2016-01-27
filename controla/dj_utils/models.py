from django.db import models


class BaseModel(models.Model):
    """ All models must inherit from BaseModel """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(verbose_name=u"Fecha de creación",
                                      auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=u"Fecha de modificación",
                                       auto_now=True)
