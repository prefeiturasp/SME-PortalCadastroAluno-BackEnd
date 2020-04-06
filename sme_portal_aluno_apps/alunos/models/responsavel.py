import logging
from django.core import validators
from django.db import models

from sme_portal_aluno_apps.core.models_abstracts import ModeloBase
from ..tasks import enviar_email_solicitacao_uniforme
from ...eol_servico.utils import EOLService
from .validators import phone_validation, cpf_validation

log = logging.getLogger(__name__)


class Responsavel(ModeloBase):
    # Status Choice
    STATUS_ATUALIZADO_EOL = 'ATUALIZADO_EOL'
    STATUS_ATUALIZADO_VALIDO = 'ATUALIZADO_VALIDO'
    STATUS_DIVERGENTE = 'DIVERGENTE'
    STATUS_DESATUALIZADO = 'DESATUALIZADO'
    STATUS_PENDENCIA_RESOLVIDA = 'PENDENCIA_RESOLVIDA'

    STATUS_NOMES = {
        STATUS_ATUALIZADO_EOL: 'Cadastro Atualizado no EOL',
        STATUS_ATUALIZADO_VALIDO: 'Cadastro Atualizado e validado',
        STATUS_DIVERGENTE: 'Cadastro Divergente',
        STATUS_DESATUALIZADO: 'Cadastro Desatualizado',
        STATUS_PENDENCIA_RESOLVIDA: 'Cadastro com Pendência Resolvida',
    }

    STATUS_CHOICES = (
        (STATUS_ATUALIZADO_EOL, STATUS_NOMES[STATUS_ATUALIZADO_EOL]),
        (STATUS_ATUALIZADO_VALIDO, STATUS_NOMES[STATUS_ATUALIZADO_VALIDO]),
        (STATUS_DIVERGENTE, STATUS_NOMES[STATUS_DIVERGENTE]),
        (STATUS_DESATUALIZADO, STATUS_NOMES[STATUS_DESATUALIZADO]),
        (STATUS_PENDENCIA_RESOLVIDA, STATUS_NOMES[STATUS_PENDENCIA_RESOLVIDA]),
    )

    # Vinculo Choice
    VINCULO_MAE = 1
    VINCULO_PAI = 2
    VINCULO_RESPONSAVEL_LEGAL = 3
    VINCULO_ALUNO_MAIOR_IDADE = 4

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

    vinculo = models.IntegerField(
        'Vínculo',
        choices=VINCULO_CHOICES,
        default=VINCULO_RESPONSAVEL_LEGAL
    )

    codigo_eol_aluno = models.CharField("Código EOL do Aluno", max_length=10, blank=True, null=True)

    nome = models.CharField("Nome do Responsável", max_length=255, blank=True, null=True)

    cpf = models.CharField(
        "CPF", max_length=11, blank=True, null=True, validators=[cpf_validation])

    email = models.CharField(
        "E-mail", max_length=255, validators=[validators.EmailValidator()], blank=True, null=True
    )

    nao_possui_email = models.BooleanField(default=False)

    ddd_celular = models.CharField("DDD Celular", max_length=4, blank=True, null=True)

    celular = models.CharField("Número Celular", validators=[phone_validation], max_length=9, blank=True, null=True)

    nao_possui_celular = models.BooleanField(default=False)

    data_nascimento = models.DateField("Data de Nascimento", blank=True, null=True)

    nome_mae = models.CharField("Nome da Mãe do Responsável", max_length=255, blank=True, null=True)

    status = models.CharField(
        'status',
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_ATUALIZADO_VALIDO
    )

    def enviar_email(self):
        if self.email:
            nome_aluno = self.alunos.nome
            if self.status == 'DIVERGENTE':
                log.info(f'Enviando email divergencia para: {self.email}.')
                enviar_email_solicitacao_uniforme.delay(
                    'Divergência nos dados informados', 'email_divergencia_cpf', self.email, {'nome': nome_aluno,
                                                                                              'id': self.id})
            else:
                log.info(f'Enviando email confirmação para: {self.email}.')
                enviar_email_solicitacao_uniforme.delay(
                    'Obrigado por solicitar o uniforme escolar', 'email_confirmacao_pedido', self.email,
                    {'nome': nome_aluno, 'id': self.id})
        else:
            log.info('Não possui e-mail para envio')

    def atualizar_responsavel_no_eol(self):
        EOLService.atualizar_dados_responsavel(self.codigo_eol_aluno, str(self.vinculo), self.nome, self.cpf,
                                               self.ddd_celular, self.celular, self.email, self.nome_mae,
                                               str(self.data_nascimento))

    def __str__(self):
        return f"{self.nome} - Cod. EOL Aluno: {self.codigo_eol_aluno}"

    class Meta:
        verbose_name = "Responsavel"
        verbose_name_plural = "Responsaveis"
