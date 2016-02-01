from datetime import datetime, timedelta

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from frontend.views.mixins import SupervisorViewMixin
from frontend.views.base import BaseReasignarPersonalView, BaseReportView
from frontend.stats import (porcentaje_asistencia_proyecto, porcentaje_actividad,
                            porcentaje_asistencia_persona, evolucion_registros_asistencia,
                            get_datos_porcentuales, get_asistencia_persona)
from frontend.excel import ExportToExcel


class IndexProyect(SupervisorViewMixin, TemplateView):
    template_name = "frontend/dashboard_supervisor.html"

    def get_context_data(self, **kwargs):
        data = super(IndexProyect, self).get_context_data(**kwargs)
        data["perc_asis_proyecto"] = porcentaje_asistencia_proyecto()
        data["perc_no_ocioso"] = porcentaje_actividad()
        data["perc_asis_persona"] = porcentaje_asistencia_persona()
        hoy = datetime.now()
        data["graf_evolucion"], data["table_evolucion"] = evolucion_registros_asistencia(hoy + timedelta(-7), hoy)
        return data


class DatosPorcentualesView(BaseReportView, TemplateView):
    template_name = "frontend/datos_porcentuales_supervisor.html"

    def get_context_data(self, **kwargs):
        data = super(DatosPorcentualesView, self).get_context_data(**kwargs)
        data["table"], data["summary"] = get_datos_porcentuales(data["fecha_desde"], data["fecha_hasta"])
        return data


class AsistenciaPorPersonaView(BaseReportView, TemplateView):
    template_name = "frontend/asistenca_persona_supervisor.html"

    def get_context_data(self, **kwargs):
        data = super(AsistenciaPorPersonaView, self).get_context_data(**kwargs)
        data["table"] = get_asistencia_persona(data["fecha_desde"], data["fecha_hasta"])
        return data


class ReasignarPersonalView(SupervisorViewMixin, BaseReasignarPersonalView):

    def get_success_url(self):
        return reverse_lazy('supervisor_frontend:reasignar_personal')


class ExportDatosPorcentualesView(BaseReportView, TemplateView):
    def get_context_data(self, **kwargs):
        data = super(ExportDatosPorcentualesView, self).get_context_data(**kwargs)
        data["table"], _ = get_datos_porcentuales(data["fecha_desde"], data["fecha_hasta"])
        return data

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
        xlsx_data = ExportToExcel().fill_datos_porcentuales(self.get_context_data(**kwargs))
        response.write(xlsx_data)
        return response


class ExportAsistenciaPersonaView(BaseReportView, TemplateView):
    def get_context_data(self, **kwargs):
        data = super(ExportAsistenciaPersonaView, self).get_context_data(**kwargs)
        data["table"] = get_asistencia_persona(data["fecha_desde"], data["fecha_hasta"])
        return data

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
        xlsx_data = ExportToExcel().fill_asistencia_personas(self.get_context_data(**kwargs))
        response.write(xlsx_data)
        return response


index = IndexProyect.as_view()
reasignar_personal = ReasignarPersonalView.as_view()
datos_porcentuales = DatosPorcentualesView.as_view()
asistencia_persona = AsistenciaPorPersonaView.as_view()
export_porcentual = ExportDatosPorcentualesView.as_view()
export_asistencia = ExportAsistenciaPersonaView.as_view()