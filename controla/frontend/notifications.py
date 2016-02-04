from dj_utils.email import send_html_mail
from users.models import User
from frontend.reports import PdfPrintAltaAsistencia


def send_notification(asistencia, **kwargs):
    user = asistencia.proyecto.responsable_rel.persona.usuario
    to = []
    if user.email and user.notificar_alta_individual:
        to.append(asistencia.proyecto.responsable_rel.persona.usuario.email)
    cc = list(User.objects.filter(rol=User.SUPERVISOR, notificar_alta_individual=True).values_list('email', flat=True))
    pdf = PdfPrintAltaAsistencia().get_pdf(asistencia)
    if any([to, cc, ]):
        send_html_mail(subject="Alta de asistencia - {}".format(asistencia.proyecto),
                       template_name='email/send_notification.html',
                       dictionary={'object': asistencia}, to=to, cc=cc,
                       attachments=[{'name': asistencia.filename_report,
                                     'content': pdf,
                                     'content_type': 'application/pdf'}])
