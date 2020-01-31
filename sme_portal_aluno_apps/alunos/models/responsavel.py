from django.core import validators
from django.db import models

from sme_portal_aluno_apps.core.models_abstracts import ModeloBase


class Responsavel(ModeloBase):
    # Status Choice
    STATUS_ATUALIZADO = 'ATUALIZADO'
    STATUS_DIVERGENTE = 'DIVERGENTE'
    STATUS_ERRO = 'ERRO'

    STATUS_NOMES = {
        STATUS_ATUALIZADO: 'Atualizado',
        STATUS_DIVERGENTE: 'Divergente',
        STATUS_ERRO: 'Erro',
    }

    STATUS_CHOICES = (
        (STATUS_ATUALIZADO, STATUS_NOMES[STATUS_ATUALIZADO]),
        (STATUS_DIVERGENTE, STATUS_NOMES[STATUS_DIVERGENTE]),
        (STATUS_ERRO, STATUS_NOMES[STATUS_ERRO]),
    )

    # Vinculo Choice
    VINCULO_MAE = 'MAE'
    VINCULO_PAI = 'PAI'
    VINCULO_RESPONSAVEL_LEGAL = 'RESPONSAVEL_LEGAL'
    VINCULO_ALUNO_MAIOR_IDADE = 'ALUNO_MAIOR_IDADE'

    VINCULO_NOMES = {
        VINCULO_MAE: 'Mãe',
        VINCULO_PAI: 'Pai',
        VINCULO_RESPONSAVEL_LEGAL: 'Responsável Legal',
        VINCULO_ALUNO_MAIOR_IDADE: 'Aluno Maior de Idade',
    }

    VINCULO_CHOICES = (
        (VINCULO_MAE, VINCULO_NOMES[VINCULO_MAE]),
        (VINCULO_PAI, VINCULO_NOMES[VINCULO_PAI]),
        (VINCULO_RESPONSAVEL_LEGAL, VINCULO_NOMES[VINCULO_RESPONSAVEL_LEGAL]),
        (VINCULO_ALUNO_MAIOR_IDADE, VINCULO_NOMES[VINCULO_ALUNO_MAIOR_IDADE]),
    )

    vinculo = models.CharField(
        'status',
        max_length=15,
        choices=VINCULO_CHOICES,
        default=VINCULO_RESPONSAVEL_LEGAL
    )

    nome = models.CharField("Nome do Responsável", max_length=255, blank=True, null=True)

    cpf = models.CharField(
        "CPF", max_length=11, blank=True, null=True, unique=True, validators=[validators.MinLengthValidator(11)])

    email = models.CharField(
        "E-mail", max_length=255, validators=[validators.EmailValidator()], blank=True, null=True, default="",
        unique=True
    )

    ddd_celular_responsavel = models.CharField("DDD Tel. Celular", max_length=4, blank=True, null=True)
    celular = models.CharField("Número Tel. Celular", max_length=9, blank=True, null=True)

    ddd_telefone_fixo = models.CharField("DDD Tel. Fixo", max_length=4, blank=True, null=True)
    telefone_fixo = models.CharField("Numero Tel. Fixo", max_length=9, blank=True, null=True)

    ddd_telefone_comercial = models.CharField("DDD Tel. Comercial", max_length=4, blank=True, null=True)
    telefone_comercial = models.CharField("Numero Tel. Comercial", max_length=9, blank=True, null=True)
    ramal_telefone_comercial = models.CharField("Ramal", max_length=4, blank=True, null=True)

    data_nascimento = models.DateField("Data de Nascimento", blank=True, null=True)

    nome_mae = models.CharField("Nome da Mãe do Responsável", max_length=255, blank=True, null=True)

    status = models.CharField(
        'status',
        max_length=15,
        choices=STATUS_CHOICES,
        default=STATUS_ATUALIZADO
    )

    def __str__(self):
        return f"{self.nome} - {self.email}"

    class Meta:
        verbose_name = "Responsavel"
        verbose_name_plural = "Responsaveis"
