from django import forms
from django.forms.formsets import formset_factory
from django.utils import timezone

from autocomplete_light import ModelChoiceField

from modelo.models import Asistencia, RegistroAsistencia, Proyecto, Persona, Estado
from users.models import User


class AltaAsistenciaForm(forms.ModelForm):
    proyecto = forms.ModelChoiceField(Proyecto.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Asistencia
        fields = ('proyecto', )


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
