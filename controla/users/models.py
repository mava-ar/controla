from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history import register

from dj_utils.models import BaseModel


class User(AbstractUser, BaseModel):
    """
    """
    SUPERVISOR = 1
    RESPONSABLE = 2
    ROLES = (
        (1, 'Supervisor'),
        (2, 'Responsable'),
    )

    rol = models.SmallIntegerField("rol", choices=ROLES, default=RESPONSABLE)
    cambia_personal = models.BooleanField("¿Puede reasignar personas a proyectos?", default=False,
                                          help_text="Al l habilitar esta opción (con rol RESPONSABLE), el usuario "
                                                    "puede cambiar el proyecto al cuál está asignado una persona.")

    @property
    def is_supervisor(self):
        return self.rol == User.SUPERVISOR


register(User)
