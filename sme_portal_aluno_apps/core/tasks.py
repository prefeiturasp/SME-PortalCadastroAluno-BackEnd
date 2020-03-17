from datetime import timedelta

from celery.schedules import crontab
from celery.task import periodic_task

from sme_portal_aluno_apps.core.helpers.enviar_email import enviar_email_html
from sme_portal_aluno_apps.core.models import Email


@periodic_task(run_every=crontab(hour=4, minute=0))
def enviar_emails_engasgados():
    emails = Email.objects.filter(enviado=False)
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
