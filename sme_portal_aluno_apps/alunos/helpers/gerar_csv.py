import logging
import environ
import csv
import zipfile

from os.path import join
from django.db.models import Value as V
from django.db.models.functions import Concat
from djqscsv import write_csv, generate_filename
from os.path import basename
from datetime import date

from ...core.utils import url
from ..models.responsavel import Responsavel
from ...core.helpers.enviar_email import enviar_email_mp
from config.settings.base import MEDIA_ROOT

env = environ.Env()
log = logging.getLogger(__name__)


def gerar_csv_mp():
    qs = Responsavel.objects.annotate(get_celular=Concat('ddd_celular', V(' '), 'celular')).filter(
        status=Responsavel.STATUS_ATUALIZADO_EOL, enviado_para_mercado_pago=False).values(
        'nome', 'alunos__nome', 'codigo_eol_aluno', 'cpf', 'get_celular', 'vinculo', 'data_nascimento',
        'nome_mae', 'status', 'nao_possui_celular', 'nao_possui_email'
    )
    qtd_linhas_qs = qs.count()

    nome_arquivo = generate_filename(qs, append_datestamp=True)
    path = join(MEDIA_ROOT, nome_arquivo)
    zip_obj = zipfile.ZipFile(path.replace('.csv', '.zip'), 'w')

    log.info('Inicia geração de arquivo CSV.')
    with open(path, 'wb') as csv_file:
        write_csv(qs, csv_file,
                  field_header_map={'nome': 'nome_responsavel',
                                    'alunos__nome': 'nome_aluno',
                                    'get_celular': 'celular',
                                    'nome_mae': 'nome_mae_responsavel'
                                    },
                  use_verbose_names=False)

    file = open(path)
    reader = csv.reader(file)
    qtd_linhas_arquivo = len(list(reader)) - 1  # qtd de linhas menos o cabeçario
    log.info(f'CSV gerado: {nome_arquivo} - Quantidade de linhas: {qtd_linhas_arquivo}')
    log.info('Comprimindo arquivo')
    zip_obj.write(path, basename(path))

    if qtd_linhas_qs == qtd_linhas_arquivo and qtd_linhas_qs > 0:
        log.info('Inicia Atualização dos registros para: enviado_para_mercado_pago = True')
        for responsavel in qs:
            obj_responsavel = Responsavel.objects.get(codigo_eol_aluno=responsavel.get('codigo_eol_aluno'))
            obj_responsavel.enviado_para_mercado_pago = True
            obj_responsavel.data_envio_mercado_pago = date.today()
            obj_responsavel.save()

        log.info('Inicia envio de e-mail para o MP')
        # TODO: Definir tipo de envio: via link ou anexo
        enviar_email_mp(
            assunto=f'Lista de novos beneficiarios - {date.today()}',
            mensagem=(f'E-mail automatico. Não responda. ' +
                      f'Clique neste link para fazer download do csv: ' +
                      f'{url(nome_arquivo)}'),
            csv=url(nome_arquivo)
        )
    else:
        # TODO: Verificar uma forma de guardar essa informação no banco
        log.info(f'Divergencia no número de linhas da query ({qtd_linhas_qs}) com o número de '
                 f'linhas do arquivo gerado ({qtd_linhas_arquivo}) ou query sem registro. '
                 'Registros não foram atualizados e e-mail não foi enviado.')
