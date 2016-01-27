from autocomplete_light import AutocompleteModelBase, register

from .models import Persona


class PersonaAutocomplete(AutocompleteModelBase):
    search_fields = ['^nombre', 'apellido']
    model = Persona

    attrs = {
        'data-autcomplete-minimum-characters': 0,
        'placeholder': "Comience a escribir el nombre...",
    }

    def choices_for_request(self):
        self.choices = self.choices.filter(fecha_baja=None)
        return super(PersonaAutocomplete, self).choices_for_request()

register(PersonaAutocomplete)
