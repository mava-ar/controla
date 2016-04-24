from django.contrib import admin
from django.db.models import Q

from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ExportActionModelAdmin

from .models import Estado, Proyecto, CCT, Persona, Asistencia, RegistroAsistencia, Responsable, MovimientoPersona
from .actions import dar_de_baja
from .admin_filters import PersonaBajaFilter


@admin.register(Estado)
class EstadoAdmin(SimpleHistoryAdmin):
    list_display = ('situacion', 'codigo', 'observaciones', )
    list_display_links = ('codigo', )


@admin.register(Proyecto)
class ProyectoAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    list_display = ('nombre', 'codigo', 'total_personas', 'responsable', 'activo_status')
    search_fields = ('nombre', 'codigo', )
    ordering = ('fecha_baja', )

    actions = [dar_de_baja, ]
    dar_de_baja.short_description = "Dar de baja"

    def activo_status(self, obj):
        return obj.activo
    activo_status.boolean = True
    activo_status.short_description = "¿Activo?"

    def responsable(self, obj):
        if not obj.responsable_rel is None:
            return obj.responsable_rel.persona
        else:
            return ""

    def get_actions(self, request):
        actions = super(ProyectoAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        return Proyecto.all_proyects.all()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(CCT)
class CCTAdmin(SimpleHistoryAdmin):
    list_display = ('nombre', 'total_personas', )


class MovimientoPersonaInlineAdmin(admin.TabularInline):
    extra = 0
    can_delete = False
    model = MovimientoPersona
    fields = ('persona', 'situacion', 'fechahora', 'usuario')
    readonly_fields = ('persona', 'situacion', 'fechahora', 'usuario')

    def has_add_permission(self, request):
        return False


@admin.register(Persona)
class PersonaAdmin(SimpleHistoryAdmin):
    list_display = ('legajo', 'apellido', 'nombre', 'cuil', 'cct', 'proyecto', 'activo_status', )
    search_fields = ('apellido', 'nombre',)
    list_filter = ('cct', 'proyecto', PersonaBajaFilter, )
    inlines = [MovimientoPersonaInlineAdmin, ]
    actions = [dar_de_baja, ]
    dar_de_baja.short_description = "Dar de baja"

    def get_queryset(self, request):
        return Persona.all_persons.all()

    def activo_status(self, obj):
        return obj.activo
    activo_status.boolean = True
    activo_status.short_description = "¿Activa?"

    def get_actions(self, request):
        actions = super(PersonaAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class RegistroAsistenciaInlineAdmin(admin.TabularInline):
    extra = 0
    can_delete = False
    model = RegistroAsistencia
    fields = ('persona', 'estado', )
    readonly_fields = ('persona', )

    def has_add_permission(self, request):
        return False


@admin.register(Asistencia)
class AsistenciaAdmin(SimpleHistoryAdmin):
    list_display = ("proyecto", "fecha", "total_items", )
    list_filter = ("proyecto", 'fecha', )
    inlines = [RegistroAsistenciaInlineAdmin, ]
    fields = ('fecha', 'proyecto', )

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_add_permission(self, request):
        return False

@admin.register(Responsable)
class ResponsableAdmin(SimpleHistoryAdmin):
    list_display = ("persona", "proyecto", )
    list_display_links = ('persona', 'proyecto', )
    list_filter = ("proyecto", 'persona', )
    ordering = ('persona', 'proyecto', )

    def get_queryset(self, request):
        # no muestro responsable con personas o proyectos dados de baja
        return Responsable.objects.exclude(Q(persona__fecha_baja__isnull=False) | Q(proyecto__fecha_baja__isnull=False))