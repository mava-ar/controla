from django.db import models
from django.apps import apps


class ProyectoManager(models.Manager):

    def get_base_queryset(self):
        return super(ProyectoManager, self).get_queryset()

    def get_queryset(self):
        return super(ProyectoManager, self).get_queryset().filter(fecha_baja=None)


class ProyectoConPersonasManager(ProyectoManager):
    def get_queryset(self):
        Persona = apps.get_model("modelo", "Persona")
        # Desde personas, selecciono los ids de proyectos con personas
        con_personas = set(Persona.objects.values_list('proyecto_id', flat=True))
        return super(ProyectoConPersonasManager, self).get_queryset().filter(pk__in=con_personas)


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