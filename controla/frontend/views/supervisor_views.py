from datetime import datetime, timedelta
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from frontend.views.mixins import SupervisorViewMixin
from frontend.views.base import BaseReasignarPersonalView
from frontend.stats import (porcentaje_asistencia_proyecto, porcentaje_actividad,
                            porcentaje_asistencia_persona, evolucion_registros_asistencia)


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

class ReasignarPersonalView(SupervisorViewMixin, BaseReasignarPersonalView):

    def get_success_url(self):
        return reverse_lazy('supervisor_frontend:reasignar_personal')


index = IndexProyect.as_view()
reasignar_personal = ReasignarPersonalView.as_view()