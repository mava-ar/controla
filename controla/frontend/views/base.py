from datetime import datetime
from django.contrib import messages
from django.contrib.auth.views import logout as django_logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.db import IntegrityError
from django.db.transaction import atomic
from django.views.generic import RedirectView, TemplateView, CreateView, DetailView
from django.http import HttpResponseRedirect
from django.conf import settings

from dj_utils.views import AuthenticatedMixin
from modelo.models import Asistencia, RegistroAsistencia, Proyecto, Persona
from users.models import User
from frontend.forms import ReasignarPersonalForm, AltaAsistenciaForm, RegistroAsistenciaFormSet
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


class BaseAltaAsistenciaView(CreateView):
    template_name = "frontend/alta_asistencia.html"
    form_class = AltaAsistenciaForm

    def get_details_asistencia_url(self, pk):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        # averiguo si ya tomo la asistencia hoy
        asistencia = Asistencia.objects.filter(proyecto=kwargs.get(self.pk_url_kwarg), fecha=datetime.now())
        if asistencia:
            messages.add_message(self.request, messages.INFO,
                                 "Mostrardo la asistencia para el día de la fecha.")
            # muestro la asistencia del día
            return HttpResponseRedirect(self.get_details_asistencia_url(asistencia[0].pk))
        return super(BaseAltaAsistenciaView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(BaseAltaAsistenciaView, self).get_context_data(**kwargs)
        pk = self.kwargs.get(self.pk_url_kwarg)
        proyecto = Proyecto.objects.get(pk=pk)
        personas = dict(
                [ (x["pk"], "{} {}".format(x["nombre"], x["apellido"]) ) for x in Persona.objects.filter(
                        proyecto=proyecto).values('pk','nombre', 'apellido') ]
        )
        data["proyecto"] = proyecto
        data["personas"] = personas
        if "formsets" not in kwargs:
            estado = settings.ESTADO_DEFAULT
            initial = [{ 'persona': k, 'estado': estado} for k,v in personas.items()]
            data['formsets'] = RegistroAsistenciaFormSet(initial=initial)
        return data

    def get_form_kwargs(self, **kwargs):
        kwargs = super(BaseAltaAsistenciaView, self).get_form_kwargs(**kwargs)
        kwargs['initial']['proyecto'] = Proyecto.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formsets = RegistroAsistenciaFormSet(self.request.POST)
        if form.is_valid() and formsets.is_valid():
            return self.form_valid(form, formsets)
        else:
            return self.form_invalid(form, formsets)

    def form_invalid(self, form, formsets):
        return self.render_to_response(
            self.get_context_data(form=form, formsets=formsets))

    def form_valid(self, form, formsets):
        try:
            with atomic():
                self.object = form.save(commit=False)
                self.object.fecha = datetime.now()
                self.object.save()
                for f in formsets:
                    reg = RegistroAsistencia()
                    reg.persona = f.cleaned_data["persona"]
                    reg.asistencia = self.object
                    if f.cleaned_data["estado"]:
                        reg.estado = f.cleaned_data["estado"]
                    reg.save()
        except IntegrityError:
            self.form_invalid(form, formsets)

        return HttpResponseRedirect(self.get_success_url())


class BaseDetailAsistenciaView(DetailView):
    model = Asistencia
    template_name = "frontend/ver_asistencia.html"


index = RedirectRolView.as_view()
