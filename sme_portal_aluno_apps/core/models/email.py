from django.db import models

from ..models_abstracts import ModeloBase


class Email(ModeloBase):
    enviado = models.BooleanField("Enviado?", default=False)
    enviar_para = models.CharField("Enviar Para", max_length=255, blank=True, null=True)
    assunto = models.CharField("Assunto", max_length=255, blank=True, null=True)
    body = models.TextField("Enviar Para",blank=True, null=True)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
