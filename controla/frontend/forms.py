from datetime import datetime
from django import forms
from django.forms.models import inlineformset_factory
from django.forms.formsets import formset_factory

from autocomplete_light import ModelChoiceField

from modelo.models import Asistencia, RegistroAsistencia, Proyecto, Persona, Estado


class AltaAsistenciaForm(forms.ModelForm):
    proyecto = forms.ModelChoiceField(Proyecto.objects.filter(fecha_baja=None), widget=forms.HiddenInput())

    class Meta:
        model = Asistencia
        fields = ('proyecto', )


class RegistroAsistenciaForm(forms.Form):
    persona = forms.ModelChoiceField(queryset=Persona.objects.all(), widget=forms.HiddenInput())
    estado = forms.ModelChoiceField(queryset=Estado.objects.all(), required=False)


RegistroAsistenciaFormSet = formset_factory(RegistroAsistenciaForm, extra=0)


class ReasignarPersonal(forms.ModelForm):
    proyecto = forms.ModelChoiceField(Proyecto.objects.filter(fecha_baja=None), widget=forms.HiddenInput())

    class Meta:
        model = Persona
        fields = ('proyecto', )


class ReasignarPersonalForm(forms.Form):
    proyecto = forms.ModelChoiceField(Proyecto.objects.filter(fecha_baja=None))
    persona = ModelChoiceField('PersonaAutocomplete')

    class Meta:
        fields = ('proyecto', 'persona', )