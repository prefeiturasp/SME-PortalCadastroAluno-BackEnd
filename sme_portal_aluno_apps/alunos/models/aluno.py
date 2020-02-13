from django.core import validators
from django.db import models

from sme_portal_aluno_apps.core.models_abstracts import ModeloBase
from .responsavel import Responsavel


class Aluno(ModeloBase):
    codigo_eol = models.CharField(
        "Código EOL do Aluno", max_length=7, unique=True, validators=[validators.MinLengthValidator(7)])
    data_nascimento = models.DateField("Data de Nascimento", blank=True, null=True)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.PROTECT, blank=True, null=True, related_name='alunos')

    def __str__(self):
        return self.codigo_eol

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"
