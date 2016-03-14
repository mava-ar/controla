from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import logout as django_logout
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.transaction import atomic
from django.http import HttpResponseRedirect
from django.views.generic import RedirectView, TemplateView, CreateView, DetailView, UpdateView
from django.utils import timezone

from dj_utils.dates import get_30_days, format_date
from dj_utils.views import AuthenticatedMixin
from frontend.forms import (ReasignarPersonalForm, AltaAsistenciaForm, RegistroAsistenciaFormSet,
                            NotificacionUserForm, VerAsistenciaForm, BajaPersonalForm, AltaPersonalForm, )
from frontend.notifications import send_notification
from modelo.models import Asistencia, RegistroAsistencia, Proyecto, Persona, MovimientoPersona
from users.models import User
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


class BaseBajaPersonalView(AuthenticatedMixin, TemplateView):
    template_name = 'frontend/baja_personal.html'

    def get_context_data(self, **kwargs):
        data = super(BaseBajaPersonalView, self).get_context_data(**kwargs)
        if kwargs.get("form_baja", None) is None:
            data["form_baja"] = BajaPersonalForm()
        if kwargs.get('form_alta', None) is None:
            data["form_alta"] = AltaPersonalForm()

        data["ultimas_bajas"] = MovimientoPersona.objects.filter(
            situacion=MovimientoPersona.SITUACION_BAJA).order_by('-fechahora')[:10]
        data["ultimas_altas"] = MovimientoPersona.objects.filter(
            situacion=MovimientoPersona.SITUACION_ALTA).order_by('-fechahora')[:10]
        return data

    def post(self, request, *args, **kwargs):
        sit = request.POST.get('situacion', None)
        if sit:
            if sit == '1':
                a_form = AltaPersonalForm(self.request.POST)
                if a_form.is_valid():
                    return self.form_valid(a_form)
                else:
                    return self.form_invalid(form_alta=a_form)
            elif sit == '2':
                b_form = BajaPersonalForm(self.request.POST)
                if b_form.is_valid():
                    return self.form_valid(b_form)
                else:
                    return self.form_invalid(form_baja=b_form)
            else:
                return self.form_invalid()

    def form_invalid(self, form_alta=None, form_baja=None):
        return self.render_to_response(
            self.get_context_data(form_alta=form_alta, form_baja=form_baja))

    def form_valid(self, form):
        personas = form.cleaned_data["personas"]
        if isinstance(form, BajaPersonalForm):
            situacion = MovimientoPersona.SITUACION_BAJA
            method_generar = MovimientoPersona.generar_baja
        else:
            situacion = MovimientoPersona.SITUACION_ALTA
            method_generar = MovimientoPersona.generar_alta
        for p in personas:
            method_generar(persona=p, fecha=timezone.now(), usuario=self.request.user)

        messages.add_message(self.request, messages.SUCCESS,
                             "Las siguientes personas fueron dadas de {}: {}".format(
                                 "baja" if situacion == MovimientoPersona.SITUACION_BAJA else "alta",
                                 ", ".join([str(x) for x in personas])))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        raise NotImplemented


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

    def checks_exists(self, **kwargs):
        # averiguo si ya tomo la asistencia hoy
        asistencia = Asistencia.objects.filter(proyecto=kwargs.get(self.pk_url_kwarg), fecha=datetime.now())
        if asistencia:
            messages.add_message(self.request, messages.INFO,
                                 "Mostrardo la asistencia para el día de la fecha.")
            # muestro la asistencia del día
            return HttpResponseRedirect(self.get_details_asistencia_url(asistencia[0].pk))

    def get(self, request, *args, **kwargs):
        redirect = self.checks_exists(**kwargs)
        if redirect:
            return redirect
        return super(BaseAltaAsistenciaView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(BaseAltaAsistenciaView, self).get_context_data(**kwargs)
        personas = [ (x["pk"], "{} {}".format(x["apellido"], x["nombre"]) ) for x in Persona.objects.filter(
                        proyecto=self.proyecto).values('pk', 'apellido','nombre').order_by('apellido', 'nombre')]
        registros_existente = RegistroAsistencia.objects.filter(
                persona_id__in=personas, asistencia__fecha=datetime.now()).select_related(
                "asistencia__proyecto, persona").values(
                'persona_id', 'persona__nombre', 'persona__apellido', 'estado__codigo', 'estado__situacion',
                'asistencia__proyecto__nombre')
        if registros_existente:
            aux = list()
            data["ya_registradas"] = registros_existente
            for reg in data["ya_registradas"]:
                aux.append((reg["persona_id"], "{} {}".format(reg["persona__apellido"], reg["persona__nombre"])))
            personas = [y for y in personas if y not in aux]
        data["proyecto"] = self.proyecto
        data["personas"] = dict(personas)
        if "formsets" not in kwargs:
            estado = settings.ESTADO_DEFAULT
            initial = [{ 'persona': k, 'estado': estado} for k,v in personas]
            data['formsets'] = RegistroAsistenciaFormSet(initial=initial)
        return data

    def get_form_kwargs(self, **kwargs):
        kwargs = super(BaseAltaAsistenciaView, self).get_form_kwargs(**kwargs)
        self.proyecto = Proyecto.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
        kwargs['initial']['proyecto'] =  self.proyecto
        kwargs['initial']['fecha'] = datetime.now().strftime("%d/%m/%Y")
        return kwargs

    def post(self, request, *args, **kwargs):
        redirect = self.checks_exists(**kwargs)
        if redirect:
            return redirect
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
                if not self.request.user.is_supervisor:
                    self.object.fecha = datetime.now()
                self.object.save()
                for f in formsets:
                    reg = RegistroAsistencia()
                    reg.persona = f.cleaned_data["persona"]
                    reg.asistencia = self.object
                    if f.cleaned_data["estado"]:
                        reg.estado = f.cleaned_data["estado"]
                    reg.save()
            send_notification(self.object)
        except IntegrityError:
            self.form_invalid(form, formsets)

        return HttpResponseRedirect(self.get_success_url())


class BaseDetailAsistenciaView(DetailView):
    model = Asistencia
    template_name = "frontend/ver_asistencia.html"

    def get_context_data(self, **kwargs):
        context = super(BaseDetailAsistenciaView, self).get_context_data()
        context["registros"] = self.object.items.all().order_by('persona')
        context["ya_registradas"] = RegistroAsistencia.objects.filter(
                persona__in=context["asistencia"].proyecto.personas_involucradas.all(),
                asistencia__fecha=datetime.now()).exclude(
                asistencia=context["asistencia"]).select_related("asistencia__proyecto").values(
                'persona__nombre', 'persona__apellido', 'estado__codigo', 'estado__situacion',
                'asistencia__proyecto__nombre')
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        self.object = Asistencia.objects.filter(pk=pk).prefetch_related('items__estado', 'items__persona').get()
        return self.object


class BaseNotificacionesView(AuthenticatedMixin, UpdateView):
    model = User
    form_class = NotificacionUserForm
    template_name = 'frontend/update_notification.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.instance = self.request.user
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS, "Configuración de notificaciones actualizada correctamente.")
        return HttpResponseRedirect(reverse('index'))


class BaseVerAsistenciaByDate(TemplateView):
    template_name = 'frontend/ver_asistencia_fecha.html'

    def get_queryset(self):
        return Proyecto.objects.all()

    def get_context_data(self, **kwargs):
        data = super(BaseVerAsistenciaByDate, self).get_context_data(**kwargs)
        data["proyectos"] = self.get_queryset()
        data["fecha"] = datetime.now().strftime("%d/%m/%Y")
        return data


class BaseVerAsistenciaAjaxView(TemplateView):
    template_name = "frontend/includes/_table_asistencia.html"

    def get(self, request, *args, **kwargs):
        form = VerAsistenciaForm(self.request.GET)
        data = self.get_context_data()
        try:
            if form.is_valid():
                proy = form.cleaned_data["proyecto"]
                fecha = form.cleaned_data["fecha"]
                data["object"] = Asistencia.objects.get(
                    proyecto=proy, fecha=fecha)
                data["registros"] = data["object"].items.all().order_by('persona')
        except Asistencia.DoesNotExist:
            data["object"] = None
        return self.render_to_response(data)


index = RedirectRolView.as_view()
update_notification = BaseNotificacionesView.as_view()

