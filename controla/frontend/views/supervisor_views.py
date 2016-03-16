from datetime import datetime, timedelta

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.transaction import atomic

from modelo.models import Responsable, Asistencia, Proyecto, Persona, RegistroAsistencia
from frontend.views.mixins import SupervisorViewMixin
from frontend.forms import FusionarProyectosForm
from frontend.views.base import (BaseReasignarPersonalView, BaseReportView, BaseDetailAsistenciaView,
                                 BaseAltaAsistenciaView, BaseNotificacionesView, BaseVerAsistenciaAjaxView,
                                 BaseVerAsistenciaByDate, BaseBajaPersonalView)
from frontend.stats import (porcentaje_asistencia_proyecto, porcentaje_actividad,
                            porcentaje_asistencia_persona, evolucion_registros_asistencia,
                            get_datos_porcentuales, get_asistencia_persona, get_proyectos_estados)
from frontend.excel import ExportToExcel
from frontend.reports import PdfPrintAltaAsistencia


class DashboardView(SupervisorViewMixin, TemplateView):
    template_name = "frontend/dashboard_supervisor.html"

    def get_context_data(self, **kwargs):
        hoy = datetime.now()
        data = super(DashboardView, self).get_context_data(**kwargs)
        data["perc_asis_proyecto"] = porcentaje_asistencia_proyecto(hoy)
        data["perc_no_ocioso"] = porcentaje_actividad(hoy)
        data["perc_asis_persona"] = porcentaje_asistencia_persona(hoy)

        data["graf_evolucion"], data["table_evolucion"] = evolucion_registros_asistencia(hoy + timedelta(-7), hoy)
        data["proyectos_estados"] = get_proyectos_estados(hoy)
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


class BajaPersonalView(SupervisorViewMixin, BaseBajaPersonalView):

    def get_success_url(self):
        return reverse_lazy('supervisor_frontend:baja_personal')


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


class IndexResponsable(SupervisorViewMixin, TemplateView):
    template_name = "frontend/index_responsables.html"

    def get_context_data(self, **kwargs):
        data = super(IndexResponsable, self).get_context_data(**kwargs)
        data["responsables"] = [(x[0], "{} {}".format(x[1], x[2])) for x in
                                     Responsable.objects.values_list(
                                             'persona__pk', 'persona__apellido', 'persona__nombre').order_by('persona').distinct()]
        return data


class VerProyectosAjaxView(SupervisorViewMixin, TemplateView):
    template_name = "frontend/includes/_index_proyectos.html"

    def get_context_data(self, **kwargs):
        data = super(VerProyectosAjaxView, self).get_context_data(**kwargs)
        pk = self.request.GET.get('pk', None)
        if pk:
            data["proyectos"] = Proyecto.con_personas.filter(responsable_rel__persona_id=pk).all()
            hoy = datetime.now()
            data["asistencia_dia"] = list(Asistencia.objects.filter(
                    proyecto__in=data["proyectos"], fecha=hoy).values_list('proyecto__pk', flat=True))
        return data

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class AltaAsistenciaView(SupervisorViewMixin, BaseAltaAsistenciaView):

    def get_details_asistencia_url(self, pk):
        return reverse_lazy('supervisor_frontend:ver_asistencia', kwargs={'pk': pk})

    def get_success_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             "Asistencia enviada correctamente.")
        if self.object:
            return reverse_lazy('supervisor_frontend:ver_asistencia',
                                kwargs={'pk': self.object.pk})
        else:
            return reverse('supervisor_frontend:index')


class DetailAsistenciaView(SupervisorViewMixin, BaseDetailAsistenciaView):
    pass


class Export2PDFView(SupervisorViewMixin, BaseDetailAsistenciaView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(self.object.filename_report)
        pdf = PdfPrintAltaAsistencia().get_pdf(self.object)
        response.write(pdf)
        return response


class NotificacionesView(SupervisorViewMixin, BaseNotificacionesView):
    pass


class VerAsistenciaByDate(SupervisorViewMixin, BaseVerAsistenciaByDate):
    pass


class VerAsistenciaAjaxView(SupervisorViewMixin, BaseVerAsistenciaAjaxView):
    pass


class FusionarProyectosView(SupervisorViewMixin, FormView):
    template_name = 'admin/fusionar_proyectos.html'
    form_class = FusionarProyectosForm
    success_url = 'supervisor_frontend:fusionar_proyectos'

    def form_valid(self, form):
        p_destino = form.cleaned_data["proyecto_destino"]
        try:
            for p_fusion in form.cleaned_data["proyectos_fusion"]:
                if p_fusion == p_destino:
                    continue
                # mover personas
                Persona.objects.filter(proyecto=p_fusion).update(proyecto=p_destino)
                # mover asistencia
                try:
                    Asistencia.objects.filter(proyecto=p_fusion).update(proyecto=p_destino)
                except IntegrityError:
                    for asist in Asistencia.objects.filter(proyecto=p_fusion):
                        nueva, _ = Asistencia.objects.get_or_create(fecha=asist.fecha, proyecto=p_destino)
                        RegistroAsistencia.objects.filter(asistencia=asist).update(asistencia=nueva)
                    Asistencia.objects.filter(proyecto=p_fusion).delete()
                # Eliminar responsable
                Responsable.objects.filter(proyecto=p_fusion).delete()
                # Eliminar proyecto
                p_fusion.delete()
                messages.add_message(self.request, messages.SUCCESS,
                                     "Proyecto {} fusionado con {}.".format(p_fusion, p_destino))
            if 'nuevo_nombre' in form.cleaned_data and len(form.cleaned_data["nuevo_nombre"]) > 4:
                p_destino.nombre = form.cleaned_data["nuevo_nombre"]
                p_destino.save()
                messages.add_message(self.request, messages.SUCCESS,
                                     "Nuevo nombre del proyecto: {} .".format(p_destino.nombre))

        except Exception as e:
            return super(FusionarProyectosView, self).form_invalid(form)
        return HttpResponseRedirect(reverse(self.get_success_url()))


index = DashboardView.as_view()
reasignar_personal = ReasignarPersonalView.as_view()
baja_personal = BajaPersonalView.as_view()
datos_porcentuales = DatosPorcentualesView.as_view()
asistencia_persona = AsistenciaPorPersonaView.as_view()
export_porcentual = ExportDatosPorcentualesView.as_view()
export_asistencia = ExportAsistenciaPersonaView.as_view()
index_responsable = IndexResponsable.as_view()
ver_proyectos_ajax = VerProyectosAjaxView.as_view()
alta_asistencia = AltaAsistenciaView.as_view()
ver_asistencia = DetailAsistenciaView.as_view()
export_asistencia_pdf = Export2PDFView.as_view()
update_notification = NotificacionesView.as_view()
ver_asistencia_fecha = VerAsistenciaByDate.as_view()
ver_asistencia_ajax = VerAsistenciaAjaxView.as_view()
fusionar_proyectos = FusionarProyectosView.as_view()
