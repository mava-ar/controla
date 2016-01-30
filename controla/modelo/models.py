from django.db import models
from django.db.models.fields import related
from django.conf import settings
from simple_history.models import HistoricalRecords

from dj_utils.models import BaseModel, BaseModelWithHistory
from .managers import ProyectoManager, PersonaManager


class Estado(BaseModelWithHistory):
    """
    Representa los posibles valores para la asistencia de cada persona.

    """
    situacion = models.CharField("situación", max_length=255)
    codigo = models.CharField("código", max_length=5, unique=True)
    observaciones = models.CharField("observaciones", max_length=255,
                                     blank=True, null=True)
    no_ocioso = models.BooleanField("No está ocioso", default=False,
                                    help_text="Seleccione esta opción para indicar "
                                              "que el estado no implica ociosidad por parte del empleado")
    history = HistoricalRecords()


    class Meta:
        verbose_name = "estado"
        verbose_name_plural = "estados"
        ordering = ('situacion', )

    def __str__(self):
        return "{} - {}".format(self.codigo, self.situacion)


class Proyecto(BaseModelWithHistory):
    """
    Representa un proyecto de la empresa o Centro de Costo. Un persona es
    responsable de la asistencia.

    """
    nombre = models.CharField("nombre", max_length=255, unique=True)
    fecha_baja = models.DateField("fecha de baja", null=True, blank=True)
    history = HistoricalRecords()

    objects = ProyectoManager()
    all_proyects = models.Manager()

    class Meta:
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"

    def __str__(self):
        return self.nombre if self.nombre else "Sin nombre"

    @property
    def total_personas(self):
        return "{} personas".format(self.personas_involucradas.count())

    @property
    def activo(self):
        return self.fecha_baja is None


class Responsable(BaseModelWithHistory):
    """
    Representa al responsable del proyecto, junto a sus configuraciones.

    """
    persona = models.ForeignKey("Persona", verbose_name="persona", related_name="responsable_rel", null=True)
    proyecto = models.OneToOneField(Proyecto, verbose_name="proyecto", related_name="responsable_rel", null=True)
    history = HistoricalRecords()

    def __str__(self):
        return "{} responsable de {}".format(
            self.persona, self.proyecto
        )

    class Meta:
        verbose_name = "responsable"
        verbose_name_plural = "responsables"
        unique_together = ('persona', 'proyecto', )


class CCT(BaseModelWithHistory):
    """
    Representa un Contrato Colectivo de Trabajo.

    """
    nombre = models.CharField("nombre", max_length=255, unique=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "CCT"
        verbose_name_plural = "CCTs"

    def __str__(self):
        return self.nombre

    @property
    def total_personas(self):
        return "{} personas".format(self.personas.count())



class Persona(BaseModelWithHistory):
    """
    Representa una persona que trabaja en la empresa.
    """
    legajo = models.IntegerField("legajo", unique=True)
    apellido = models.CharField("apellido", max_length=255)
    nombre = models.CharField("nombre", max_length=255)
    cuil = models.CharField("CUIL", max_length=15)
    cct = models.ForeignKey(CCT, verbose_name="CCT", related_name="personas")
    proyecto = models.ForeignKey(Proyecto, verbose_name="proyecto",
                                 related_name="personas_involucradas")
    usuario = models.ForeignKey('users.User', verbose_name="Usuario", null=True, blank=True, related_name="persona",
                                help_text="Al asociar un usuario a la persona, este puede ingresar al sistema.")
    fecha_baja = models.DateField("fecha de baja", null=True, blank=True)
    history = HistoricalRecords()

    objects = PersonaManager()
    all_persons = models.Manager()

    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "personas"
        ordering = ("apellido", "nombre", )

    def __str__(self):
        return "{} {}".format(self.apellido, self.nombre)

    @property
    def activo(self):
        return self.fecha_baja is None


class Asistencia(BaseModelWithHistory):
    """
    Representa la asistencia para un día y proyecto específico.

    """
    fecha = models.DateField("Fecha de presentismo")
    proyecto = models.ForeignKey(Proyecto, related_name="asistencias")
    nombre_responsable = models.CharField(
        "Nombre del responsable", max_length=255,
        help_text="Se completará automaticamente con el responsable del proyecto seleccionado")
    nombre_proyecto = models.CharField(
        "Nombre del proyecto", max_length=255,
        help_text="Se completará automaticamente con el nombre del proyecto seleccionado.")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "asistencia"
        verbose_name_plural = "asistencias"
        unique_together = ('fecha', 'proyecto', )

    def __str__(self):
        return "{} - {}".format(self.fecha, self.proyecto)

    def save(self, *args, **kwargs):
        self.nombre_proyecto = self.proyecto.nombre
        try:
            if not self.nombre_responsable:
                self.nombre_responsable = "{}".format(self.proyecto.responsable_rel.persona)
        except:
            pass
        super(Asistencia, self).save(*args, **kwargs)

    @property
    def total_items(self):
        return "{} items".format(self.items.count())


class RegistroAsistencia(BaseModelWithHistory):
    """
    Representa el dato sobre la asistencia de una persona para una
    Asistencia en particular.

    """
    asistencia = models.ForeignKey(Asistencia, related_name="items")
    persona = models.ForeignKey(Persona, related_name='registro_asistencia')
    estado = models.ForeignKey(Estado, verbose_name="estado de presentismo", default=settings.ESTADO_DEFAULT)
    codigo_estado = models.CharField(
        "Código", max_length=5, help_text="Se establecerá automaticamente con "
                                          "el código del estado seleccionado.")
    observaciones = models.CharField("observaciones", max_length=255,
                                     blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "registro de asistencia"
        verbose_name_plural = "registros de asistencia"
        unique_together = ('asistencia', 'persona', )

    def __str__(self):
        return "{} - {}".format(self.persona, self.asistencia)

    def save(self, *args, **kwargs):
        self.codigo_estado = self.estado.codigo
        super(RegistroAsistencia, self).save(*args, **kwargs)
