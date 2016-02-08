from datetime import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView

from frontend.views.base import (BaseReasignarPersonalView, BaseAltaAsistenciaView, BaseDetailAsistenciaView,
                                 BaseNotificacionesView)
from frontend.views.mixins import ResponsableViewMixin
from modelo.models import Persona, Asistencia, Proyecto


class IndexProyect(ResponsableViewMixin, TemplateView):
    template_name = "frontend/index_proyectos.html"

    def get_context_data(self, **kwargs):
        data = super(IndexProyect, self).get_context_data(**kwargs)
        try:
            proyectos = [x.proyecto_id for x in self.request.user.persona.get().responsable_rel.all()]
            data["proyectos"] = Proyecto.con_personas.filter(id__in=proyectos)
            hoy = datetime.now()
            data["asistencia_dia"] = list(Asistencia.objects.filter(
                    proyecto__in=data["proyectos"], fecha=hoy).values_list('proyecto__pk', flat=True))
        except Persona.DoesNotExist as e:
            pass
        return data


class AltaAsistenciaView(ResponsableViewMixin, BaseAltaAsistenciaView):

    def get_details_asistencia_url(self, pk):
        return reverse_lazy('responsable_frontend:ver_asistencia', kwargs={'pk': pk})

    def get_success_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             "Asistencia enviada correctamente.")
        if self.object:
            return reverse_lazy('responsable_frontend:ver_asistencia',
                                kwargs={'pk': self.object.pk})
        else:
            return reverse('responsable_frontend:index')


class DetailAsistenciaView(ResponsableViewMixin, BaseDetailAsistenciaView):
    def get_queryset(self):
        proyectos = self.request.user.persona.get().responsable_rel.values_list("proyecto")
        return Asistencia.objects.filter(proyecto_id__in=proyectos)


class ReasignarPersonalView(ResponsableViewMixin, BaseReasignarPersonalView):

    def get_success_url(self):
        return reverse_lazy('responsable_frontend:reasignar_personal')


class NotificacionesView(ResponsableViewMixin, BaseNotificacionesView):
    pass


index = IndexProyect.as_view()
alta_asistencia = AltaAsistenciaView.as_view()
ver_asistencia = DetailAsistenciaView.as_view()
reasignar_personal = ReasignarPersonalView.as_view()
update_notification = NotificacionesView.as_view()
