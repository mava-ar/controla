from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.template import Context, RequestContext
from django.template.loader import render_to_string
from django.utils.translation import get_language, activate


def send_html_mail(subject, template_name, dictionary, from_email=None,
                   to=None, cc=None, bcc=None, fail_silently=False,
                   request=None, css_files=None, lang=None, attachments=[]):
    """
    Custom sned_mail for sending HTML emails rendered from a template
    Attachments debe ser un dict del tipo:
    {'name': 'nomrbe.pdf', 'content': [bytes], 'content_type': 'application/pdf'}
    """

    if lang:
        current_lang = get_language()
        activate(lang)

    if request:
        context = RequestContext(dictionary)
    else:
        context = Context(dictionary)
    message_body = render_to_string(template_name, context_instance=context)
    # message_body = Pynliner().from_string(message_body).run()

    message = EmailMessage(subject, message_body, from_email, to, bcc, cc=cc)
    message.content_subtype = 'html'
    for att in attachments:
        message.attach(att["name"], att["content"], att["content_type"])
    result = message.send(fail_silently)

    if lang:
        activate(current_lang)

    return result


