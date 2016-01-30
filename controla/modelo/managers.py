from django.db import models


class ProyectoManager(models.Manager):

    def get_base_queryset(self):
        return super(ProyectoManager, self).get_queryset()

    def get_queryset(self):
        return super(ProyectoManager, self).get_queryset().filter(fecha_baja=None)


class PersonaManager(models.Manager):

    def get_base_queryset(self):
        return super(PersonaManager, self).get_queryset()

    def get_queryset(self):
        return super(PersonaManager, self).get_queryset().filter(fecha_baja=None)
