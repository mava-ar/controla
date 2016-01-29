from django.contrib import messages
from django.contrib.auth.views import logout as django_logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.http import HttpResponseRedirect

from dj_utils.views import AuthenticatedMixin
from users.models import User
from frontend.forms import ReasignarPersonalForm


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


def logout(request):
    messages.add_message(request, messages.SUCCESS, u"Has cerrado la sesión exitosamente.")
    return django_logout(request, next_page=reverse('login'))


index = RedirectRolView.as_view()
