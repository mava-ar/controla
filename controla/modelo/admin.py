from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Estado, Proyecto, CCT, Persona, Asistencia, RegistroAsistencia, Responsable
from .actions import dar_de_baja


@admin.register(Estado)
class EstadoAdmin(SimpleHistoryAdmin):
    list_display = ('situacion', 'codigo', 'observaciones', )
    list_display_links = ('codigo', )


@admin.register(Proyecto)
class ProyectoAdmin(SimpleHistoryAdmin):
    list_display = ('nombre', 'total_personas', 'responsable', 'activo_status')
    search_fields = ('nombre', )
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


@admin.register(CCT)
class CCTAdmin(SimpleHistoryAdmin):
    list_display = ('nombre', 'total_personas', )


@admin.register(Persona)
class PersonaAdmin(SimpleHistoryAdmin):
    list_display = ('apellido', 'nombre', 'cuil', 'cct', 'proyecto', 'activo_status', )
    search_fields = ('apellido', 'nombre',)
    list_filter = ('cct', 'proyecto', )
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

@admin.register(Responsable)
class ResponsableAdmin(SimpleHistoryAdmin):
    list_display = ("proyecto", "persona", )
    list_filter = ("proyecto", 'persona', )
