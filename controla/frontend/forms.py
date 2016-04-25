from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import formset_factory
from django.utils import timezone

from autocomplete_light import ModelChoiceField

from modelo.models import Asistencia, RegistroAsistencia, Proyecto, Persona, Estado, MovimientoPersona
from users.models import User


class AltaAsistenciaForm(forms.ModelForm):
    proyecto = forms.ModelChoiceField(Proyecto.objects.all(), widget=forms.HiddenInput())
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class':'datepicker'}))

    class Meta:
        model = Asistencia
        fields = ('proyecto', 'fecha', )



class RegistroAsistenciaForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=Persona.objects.all(), widget=forms.HiddenInput())
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), required=False)


RegistroAsistenciaFormSet = formset_factory(RegistroAsistenciaForm, extra=0)


class ReasignarPersonal(forms.ModelForm):
    proyecto = forms.ModelChoiceField(Proyecto.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Persona
        fields = ('proyecto', )


class ReasignarPersonalForm(forms.Form):
    proyecto = forms.ModelChoiceField(Proyecto.objects.all())
    persona = ModelChoiceField('PersonaAutocomplete')

    class Meta:
        fields = ('proyecto', 'persona', )


class NotificacionUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('notificar_alta_individual', 'notificar_alta_diario', 'alertar_faltantes',)


class VerAsistenciaForm(forms.Form):
    proyecto = forms.ModelChoiceField(Proyecto.objects.all())
    fecha = forms.DateField(initial=timezone.now().strftime("%d/%m/%Y"))

    class Meta:
        fields = ('proyecto', 'fecha')


class BajaPersonalForm(forms.Form):

    personas = forms.ModelMultipleChoiceField(Persona.objects.all())
    situacion = forms.ChoiceField(choices=(MovimientoPersona.TIPO_SITUACION[1], ),
                                  widget=forms.HiddenInput(), initial=MovimientoPersona.SITUACION_BAJA)


class AltaPersonalForm(forms.Form):

    personas = forms.ModelMultipleChoiceField(Persona.all_persons.filter(fecha_baja__isnull=False))
    situacion = forms.ChoiceField(choices=(MovimientoPersona.TIPO_SITUACION[0], ),
                                  widget=forms.HiddenInput(), initial=MovimientoPersona.SITUACION_ALTA)


class FusionarProyectosForm(forms.Form):
    proyecto_destino = forms.ModelChoiceField(
        Proyecto.objects.all(),
        empty_label="Seleccione el proyecto destino",
        help_text="Seleccione el proyecto que recibirá todos los datos de los proyectos abajo seleccioandos.")
    proyectos_fusion = forms.ModelMultipleChoiceField(
        Proyecto.all_projects.all(), label="Seleccione todos los proyectos a fusionar",
        help_text="Seleccione todos los proyectos que fusionará con el proyecto destino. Estos proyectos serán "
                  "eliminados si el proceso es satisfactorio")
    nuevo_nombre = forms.CharField(max_length=255, required=False, min_length=4,
                                   help_text="Escriba una nuevo nombre si desea corregir el nombre del proyecto destino")

