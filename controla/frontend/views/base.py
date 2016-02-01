from datetime import datetime
from django.contrib import messages
from django.contrib.auth.views import logout as django_logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.http import HttpResponseRedirect

from dj_utils.views import AuthenticatedMixin
from users.models import User
from frontend.forms import ReasignarPersonalForm
from dj_utils.dates import get_30_days, format_date
from .mixins import SupervisorViewMixin

class RedirectRolView(AuthenticatedMixin, RedirectView):
    """
    """
    permanent = False

    def get_redirect_url(self, **kwargs):
        if self.request.user.rol == User.RESPONSABLE:
            return reverse(
                'responsable_frontend:index',

            )
        if self.request.user.rol == User.SUPERVISOR:
            return reverse(
                'supervisor_frontend:index',

            )


class BaseReasignarPersonalView(AuthenticatedMixin, TemplateView):
    template_name = "frontend/reasignar_personal.html"

    def get_context_data(self, **kwargs):
        data = super(BaseReasignarPersonalView, self).get_context_data(**kwargs)
        if not 'form' in kwargs:
            data["form"] = ReasignarPersonalForm()
        return data

    def post(self, request, *args, **kwargs):
        self.object = None
        p_form = ReasignarPersonalForm(self.request.POST)

        if p_form.is_valid():
            return self.form_valid(p_form)
        else:
            return self.form_invalid(p_form)

    def form_invalid(self, p_form):
        return self.render_to_response(
            self.get_context_data(form=p_form))

    def form_valid(self, form):
        persona = form.cleaned_data["persona"]
        proyecto = form.cleaned_data["proyecto"]
        persona.proyecto = proyecto
        persona.save()
        messages.add_message(self.request, messages.SUCCESS,
                             "{} fue asignado a {} correctamente.".format(persona, proyecto))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        raise NotImplemented


class BaseReportView(SupervisorViewMixin):
    def get_context_data(self, **kwargs):
        data = super(BaseReportView, self).get_context_data(**kwargs)

        try:
            data["fecha_desde"] = datetime.strptime(self.request.GET.get("fecha_desde"), '%d/%m/%Y')
            data["fecha_hasta"] = datetime.strptime(self.request.GET.get("fecha_hasta"), '%d/%m/%Y')
        except:
            start, end = get_30_days()
            data["fecha_desde"] = start
            data["fecha_hasta"] = end
        return data

    def dispatch(self, request, *args, **kwargs):
        if not 'fecha_desde' in request.GET:
            start, stop = get_30_days()
            return HttpResponseRedirect('%s?fecha_desde=%s&fecha_hasta=%s' % (
                request.path, format_date(start), format_date(stop)
            ))
        return super(BaseReportView, self).dispatch(request, *args, **kwargs)


def logout(request):
    messages.add_message(request, messages.SUCCESS, u"Has cerrado la sesión exitosamente.")
    return django_logout(request, next_page=reverse('login'))


index = RedirectRolView.as_view()
