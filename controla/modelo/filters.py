from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFromToRangeFilter
from django_filters.widgets import RangeWidget

from .models import RegistroAsistencia, Proyecto, Responsable, Estado


class DetallePersonaFilter(FilterSet):
    fecha = DateFromToRangeFilter(name='asistencia__fecha', widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD', 'class': 'form-control datepicker'}))
    proyecto = ModelChoiceFilter(queryset=Proyecto.objects.all(), name='asistencia__proyecto')
    nombre_responsable = CharFilter(lookup_expr='icontains', name='asistencia__nombre_responsable')

    class Meta:
        model = RegistroAsistencia
        fields = ('fecha', 'proyecto', 'nombre_responsable', 'estado')


class RegistroPorFechaProyectoFilter(FilterSet):
    fecha = DateFromToRangeFilter(
        name='asistencia__fecha', required=True, help_text="Seleccione el rango de fechas del reporte.",
        widget=RangeWidget(attrs={'placeholder': 'DD/MM/YYYY', 'class': 'form-control datepicker'}))
    proyecto = ModelChoiceFilter(
        queryset=Proyecto.objects.all(), name='asistencia__proyecto', required=False,
        help_text="Seleccione un proyecto.")

    class Meta:
        model = RegistroAsistencia
        fields = ('fecha', 'proyecto', )
