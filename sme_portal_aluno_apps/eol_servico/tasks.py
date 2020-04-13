import logging

import environ
from celery import shared_task


env = environ.Env()
log = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(TimeoutError,),
    retry_backoff=2,
    retry_kwargs={'max_retries': 8},
)
def atualizar_responsavel_no_eol(codigo_eol_aluno, vinculo, nome, cpf, ddd_celular, celular, email, nome_mae,
                                 data_nascimento):
    from ..eol_servico.utils import EOLService

    log.info(f'Chamada do metodo para atualizacao no eol')
    EOLService.atualizar_dados_responsavel(
        codigo_eol=codigo_eol_aluno,
        vinculo=vinculo,
        nome=nome,
        cpf=cpf,
        ddd_celular=ddd_celular,
        celular=celular,
        email=email,
        nome_mae=nome_mae,
        data_nascimento=data_nascimento
    )
