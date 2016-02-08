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
                                          help_text="Al habilitar esta opción, el usuario "
                                                    "puede cambiar el proyecto al cuál está asignado una persona.")
    notificar_alta_individual = models.BooleanField(
            "Notificar alta asistencia", default=True,
            help_text="Se notificará vía email el alta de asistencia de proyectos relacionados.")
    notificar_alta_diario = models.BooleanField(
            "Notificar diariamente las altas", default=False,
            help_text="Se notificará vía email, diariamente, el total de altas de asistencias."
    )
    alertar_faltantes = models.BooleanField(
        "Alertarme sobre asistencias faltantes", default=True,
        help_text="Se alertará vía email la falta de asistencias del día, si existieran.")

    @property
    def is_supervisor(self):
        return self.rol == User.SUPERVISOR


register(User)
