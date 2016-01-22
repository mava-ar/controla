from django.contrib import admin

from .models import Estado, Proyecto, CCT, Persona, Asistencia, RegistroAsistencia


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('situacion', 'codigo', 'observaciones', )
    list_display_links = ('codigo', )


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'responsable', 'total_personas', 'activo_status')

    search_fields = ('nombre', )
    ordering = ('fecha_baja', )

    def activo_status(self, obj):
        return obj.activo
    activo_status.boolean = True


@admin.register(CCT)
class CCTAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'total_personas', )


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'cuil', 'cct', 'proyecto', )
    search_fields = ('apellido', 'nombre',)
    list_filter = ('cct', 'proyecto', )


class RegistroAsistenciaInlineAdmin(admin.TabularInline):
    extra = 1
    can_delete = False
    model = RegistroAsistencia
    fields = ('persona', 'estado', )


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ("proyecto", "fecha", "total_items", )
    list_filter = ("proyecto", 'fecha', )
    inlines = [RegistroAsistenciaInlineAdmin, ]
    fields = ('fecha', 'proyecto', )
