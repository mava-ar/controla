from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy
from frontend.views.mixins import SupervisorViewMixin
from frontend.views.base import BaseReasignarPersonalView


class IndexProyect(SupervisorViewMixin, TemplateView):
    template_name = "frontend/dashboard_supervisor.html"


class ReasignarPersonalView(SupervisorViewMixin, BaseReasignarPersonalView):

    def get_success_url(self):
        return reverse_lazy('supervisor_frontend:reasignar_personal')


index = IndexProyect.as_view()
reasignar_personal = ReasignarPersonalView.as_view()