from django.core import validators
from django.db import models
from django.contrib.postgres.fields import JSONField
from sme_portal_aluno_apps.core.models_abstracts import ModeloBase


class LogConsultaEOL(ModeloBase):
    codigo_eol = models.CharField(
        "Código EOL do Aluno", max_length=7, unique=True, validators=[validators.MinLengthValidator(7)])
    json = JSONField('Lista de campos', blank=True, default={})
