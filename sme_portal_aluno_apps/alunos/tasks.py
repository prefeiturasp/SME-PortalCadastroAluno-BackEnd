from smtplib import SMTPServerDisconnected

import environ
from celery import shared_task

from ..core.helpers.enviar_email import enviar_email_html

env = environ.Env()


# https://docs.celeryproject.org/en/latest/userguide/tasks.html
@shared_task(
    autoretry_for=(SMTPServerDisconnected,),
    retry_backoff=2,
    retry_kwargs={'max_retries': 8},
)
def enviar_email_solicitacao_uniforme(assunto, template, email, contexto):
    return enviar_email_html(
        assunto=assunto,
        template=template,
        contexto=contexto,
        enviar_para=email
    )
