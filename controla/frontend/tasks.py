from __future__ import absolute_import
from datetime import timedelta

from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from mailer.engine import send_all

from modelo.models import Asistencia, Responsable, Persona, Proyecto
from frontend.reports import PdfPrintAltaAsistencia
from dj_utils.email import send_html_mail

logger = get_task_logger(__name__)


@periodic_task(run_every=timedelta(seconds=60))
def email_tasks():
    # Chequea nuevos email en la cola
    send_all()


# alerta de asistencia faltante.
@periodic_task(run_every=(crontab(minute='00', hour='11')), name="send_email_alert", ignore_result=True)
def send_email_alert():
    hoy = timezone.now()
    # para cada responsables
    for pers_pk in Responsable.objects.values_list('persona', flat=True).distinct():
        persona = Persona.objects.get(pk=pers_pk)
        realizados = Asistencia.objects.filter(
            fecha=hoy,
            proyecto__responsable_rel__persona_id=pers_pk).values_list("proyecto", flat=True)
        pendiente = Proyecto.con_personas.filter(responsable_rel__persona_id=pers_pk).exclude(id__in=realizados)
        try:
            if persona.usuario.email and persona.usuario.alertar_faltantes and pendiente:
                send_html_mail(subject="{} - Alerta de asistencia faltante".format(persona),
                               template_name='email/send_alert.html',
                               dictionary={'proyectos': pendiente, 'responsable': persona},
                               to=[persona.usuario.email],)
                logger.info("Enviando email a {}".format(persona))
        except AttributeError:
            logger.info("Persona sin usuario asociado: {}".format(persona))


# envío resumen de alta de asistencias
@periodic_task(run_every=(crontab(minute='30', hour='14')), name="send_email_all_asistencia", ignore_result=True)
def send_email_all_asistencia():
    hoy = timezone.now()
    # para cada responsables
    for pers_pk in Responsable.objects.values_list('persona', flat=True).distinct():
        persona = Persona.objects.get(pk=pers_pk)
        try:
            if persona.usuario.email and persona.usuario.notificar_alta_diario:
                realizados = Asistencia.objects.filter(fecha=hoy, proyecto__responsable_rel__persona_id=pers_pk)
                if realizados:
                    attachs = list()
                    for asis in realizados:
                        pdf = PdfPrintAltaAsistencia().get_pdf(asis)
                        attachs.append({
                            'name': asis.filename_report,
                            'content': pdf,
                            'content_type': 'application/pdf'})

                    send_html_mail(subject="Resumen de asistencia diario - ".format(hoy.strftime("d%-%m-%Y")),
                                   template_name='email/send_notification_daily.html',
                                   dictionary={'proyectos': realizados},
                                   to=[persona.usuario.email],
                                   attachments=attachs)
        except AttributeError:
            logger.info("Persona sin usuario asociado: {}".format(persona))