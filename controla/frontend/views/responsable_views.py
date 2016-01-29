from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.transaction import atomic

from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView

from frontend.forms import AltaAsistenciaForm, RegistroAsistenciaFormSet, ReasignarPersonalForm
from dj_utils.views import AuthenticatedMixin
from modelo.models import Proyecto, Persona, RegistroAsistencia, Asistencia


class IndexProyect(AuthenticatedMixin, TemplateView):
    template_name = "frontend/index.html"

    def get_context_data(self, **kwargs):
        data = super(IndexProyect, self).get_context_data(**kwargs)
        try:
            data["proyectos"] = [x.proyecto for x in self.request.user.persona.get().responsable_rel.all()]
            hoy = datetime.now()
            data["asistencia_dia"] = list(Asistencia.objects.filter(
                    proyecto__in=data["proyectos"], fecha=hoy).values_list('proyecto__pk', flat=True))
        except Persona.DoesNotExist as e:
            pass
        return data


class AltaAsistenciaView(AuthenticatedMixin, CreateView):
    template_name = "frontend/alta_asistencia.html"
    form_class = AltaAsistenciaForm

    def get(self, request, *args, **kwargs):
        # averiguo si ya tomo la asistencia hoy
        asistencia = Asistencia.objects.filter(proyecto=kwargs.get(self.pk_url_kwarg), fecha=datetime.now())
        if asistencia:
            messages.add_message(self.request, messages.INFO,
                                 "Mostrardo la asistencia para el día de la fecha.")
            # muestro la asistencia del día
            return HttpResponseRedirect(
                    reverse_lazy('frontend:ver_asistencia',
                                 kwargs={'pk': asistencia[0].pk}))
        return super(AltaAsistenciaView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(AltaAsistenciaView, self).get_context_data(**kwargs)
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
        kwargs = super(AltaAsistenciaView, self).get_form_kwargs(**kwargs)
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

    def get_success_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             "Asistencia enviada correctamente.")
        if self.object:
            return reverse_lazy('responsable_frontend:ver_asistencia',
                                kwargs={'pk': self.object.pk})
        else:
            return reverse('responsable_frontend:index')


class DetailAsistenciaView(AuthenticatedMixin, DetailView):

    model = Asistencia
    template_name = "frontend/ver_asistencia.html"

    def get_queryset(self):
        proyectos = self.request.user.persona.get().responsable_rel.values_list("proyecto")
        return Asistencia.objects.filter(proyecto_id__in=proyectos)


class ReasignarPersonalView(AuthenticatedMixin, TemplateView):
    template_name = "frontend/reasignar_personal.html"

    def get_context_data(self, **kwargs):
        data = super(ReasignarPersonalView, self).get_context_data(**kwargs)
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
        return HttpResponseRedirect(reverse_lazy('responsable_frontend:reasignar_personal'))


index = IndexProyect.as_view()
alta_asistencia = AltaAsistenciaView.as_view()
ver_asistencia = DetailAsistenciaView.as_view()
reasignar_personal = ReasignarPersonalView.as_view()
