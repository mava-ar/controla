from django.db import models


class ProyectoManager(models.Manager):

    def get_base_queryset(self):
        return super(ProyectoManager, self).get_queryset()

    def get_queryset(self):
        return super(ProyectoManager, self).get_queryset().filter(fecha_baja=None)


class ProyectoConPersonasManager(ProyectoManager):
    def get_queryset(self):
        return super(ProyectoConPersonasManager, self).get_queryset().annotate(
            pers=models.Count('personas_involucradas__pk')).filter(pers__gt=0)

class PersonaManager(models.Manager):

    def get_base_queryset(self):
        return super(PersonaManager, self).get_queryset()

    def get_queryset(self):
        return super(PersonaManager, self).get_queryset().filter(fecha_baja=None)


class RegistroAsistenciaManager(models.Manager):
    """
    Sin usar por ahora.
    """
    def get_queryset(self):
        return super(RegistroAsistenciaManager, self).get_queryset().select_related('estado')