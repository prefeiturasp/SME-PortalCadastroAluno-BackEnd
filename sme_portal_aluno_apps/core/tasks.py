from datetime import timedelta
from smtplib import SMTPServerDisconnected

from celery.schedules import crontab
from celery.task import periodic_task
from config import celery_app

from sme_portal_aluno_apps.alunos.models import Responsavel
from sme_portal_aluno_apps.core.helpers.enviar_email import enviar_email_html, enviar_email_mp
from sme_portal_aluno_apps.core.models import Email, LogEmailMercadoPago


# @periodic_task(run_every=crontab(hour=4, minute=0))
def enviar_emails_engasgados():
    emails = Email.objects.filter(enviar_para__isnull=False, enviado=False)
    EMAILS = [{"email": "nao-responda20@sme.prefeitura.sp.gov.br"},
              {"email": "nao-responda21@sme.prefeitura.sp.gov.br"},
              {"email": "nao-responda22@sme.prefeitura.sp.gov.br"},
              {"email": "nao-responda23@sme.prefeitura.sp.gov.br"},
              {"email": "nao-responda24@sme.prefeitura.sp.gov.br"},
              {"email": "nao-responda25@sme.prefeitura.sp.gov.br"},
              {"email": "nao-responda26@sme.prefeitura.sp.gov.br"},
              {"email": "nao-responda27@sme.prefeitura.sp.gov.br"}]
    for email in emails:
        contexto = {'id': email.id}
        enviar_email_html(assunto=email.assunto, template=None, contexto=contexto, enviar_para=email.enviar_para,
                          html_salvo=email.body, lista_emails=EMAILS)


def enviar_emails_cadastros_divergentes():
    responsaveis = Responsavel.objects.filter(status="DIVERGENTE", email__isnull=False)
    for responsavel in responsaveis:
        responsavel.enviar_email()


@celery_app.task(
    autoretry_for=(SMTPServerDisconnected,),
    retry_backoff=2,
    retry_kwargs={'max_retries': 8},
)
def enviar_emails_engasgados_mp():
    emails = LogEmailMercadoPago.objects.filter(enviar_para__isnull=False, enviado=False)

    for email in emails:
        enviar_email_mp(assunto=email.assunto, mensagem=email.mensagem, csv=email.csv)
