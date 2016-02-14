from django.contrib.admin import SimpleListFilter

from .models import Responsable


class PersonaBajaFilter(SimpleListFilter):
    title = 'estado'
    parameter_name = 'persona'

    def lookups(self, request, model_admin):

        return [(True, "Activa"), (False, "De baja"), ]

    def queryset(self, request, queryset):
        if self.value():
            value = self.value() == 'True'
            if value:
                return queryset.filter(fecha_baja=None)
            else:
                return queryset.filter(fecha_baja__isnull=False)
        else:
            return queryset
