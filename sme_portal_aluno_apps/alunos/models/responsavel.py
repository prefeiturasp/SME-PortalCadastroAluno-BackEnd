from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from sme_portal_aluno_apps.core.models_abstracts import ModeloBase
from ..tasks import enviar_email_confirmacao_atualizacao
from .validators import phone_validation


class Responsavel(ModeloBase):
    # Status Choice
    STATUS_ATUALIZADO = 'ATUALIZADO'
    STATUS_PENDENTE = 'PENDENTE'
    STATUS_DIVERGENTE = 'DIVERGENTE'
    STATUS_ERRO = 'ERRO'

    STATUS_NOMES = {
        STATUS_ATUALIZADO: 'Atualizado',
        STATUS_PENDENTE: 'Pendente',
        STATUS_DIVERGENTE: 'Divergente',
        STATUS_ERRO: 'Erro',
    }

    STATUS_CHOICES = (
        (STATUS_ATUALIZADO, STATUS_NOMES[STATUS_ATUALIZADO]),
        (STATUS_PENDENTE, STATUS_NOMES[STATUS_PENDENTE]),
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
        'Vínculo',
        max_length=20,
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

    ddd_celular = models.CharField("DDD Tel. Celular", max_length=4, blank=True, null=True)
    celular = models.CharField("Número Tel. Celular", validators=[phone_validation], max_length=9, blank=True, null=True)

    data_nascimento = models.DateField("Data de Nascimento", blank=True, null=True)

    nome_mae = models.CharField("Nome da Mãe do Responsável", max_length=255, blank=True, null=True)

    status = models.CharField(
        'status',
        max_length=15,
        choices=STATUS_CHOICES,
        default=STATUS_PENDENTE
    )

    def __str__(self):
        return f"{self.nome} - {self.email}"

    class Meta:
        verbose_name = "Responsavel"
        verbose_name_plural = "Responsaveis"


@receiver(post_save, sender=Responsavel)
def proponente_post_save(instance, created, **kwargs):
    if created and instance and instance.email:
        enviar_email_confirmacao_atualizacao.delay(instance.email, {'data_encerramento': 'xx/xx'})
