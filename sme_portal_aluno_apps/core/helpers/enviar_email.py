import logging

import environ
from des.models import DynamicEmailConfiguration
from django.core.mail import send_mail, EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import render_to_string

from sme_portal_aluno_apps.core.models import Email, ListaEmail

logger = logging.getLogger(__name__)

env = environ.Env()


def enviar_email(assunto, mensagem, enviar_para):
    try:
        config = DynamicEmailConfiguration.get_solo()
        email_sme = Email.objects.create(enviar_para=enviar_para, assunto=assunto, body=mensagem)
        send_mail(
            subject=assunto,
            message=mensagem,
            from_email=config.from_email or None,
            recipient_list=[enviar_para]
        )
        email_sme.enviado = True
        email_sme.save()
    except Exception as err:
        logger.error(str(err))


def enviar_email_html(assunto, template, contexto, enviar_para):
    try:

        config = DynamicEmailConfiguration.get_solo()
        msg_html = render_to_string(f"email/{template}.html", contexto)
        emails = ListaEmail.objects.all()
        email_utilizado = emails[contexto.get('id') % len(emails)].email
        config.from_email = email_utilizado
        config.username = email_utilizado
        msg = EmailMessage(
            subject=assunto, body=msg_html,
            from_email=config.from_email or None,
            bcc=(enviar_para,),
            connection=EmailBackend(**config.__dict__)
        )
        msg.content_subtype = "html"  # Main content is now text/html
        email_sme = Email.objects.create(enviar_para=enviar_para, assunto=assunto, body=msg_html)
        msg.send()
        email_sme.enviado = True
        email_sme.save()

    except Exception as err:
        logger.error(str(err))
