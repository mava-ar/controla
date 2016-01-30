from datetime import datetime
from django.db import models



class BaseModel(models.Model):
    """ All models must inherit from BaseModel """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(verbose_name=u"Fecha de creación",
                                      auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name=u"Fecha de modificación",
                                       auto_now=True)


class BaseModelWithHistory(BaseModel):
    __history_date = None

    class Meta:
        abstract = True

    @property
    def _history_date(self):
        if self.__history_date:
            return self.__history_date
        else:
            return datetime.now()

    @_history_date.setter
    def _history_date(self, value):
        self.__history_date = value
