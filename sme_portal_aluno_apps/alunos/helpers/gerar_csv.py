import logging
import csv

from os.path import join
from django.db.models import Value as V
from django.db.models.functions import Concat
from djqscsv import write_csv, generate_filename

from ..models.responsavel import Responsavel
from config.settings.base import MEDIA_ROOT

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
    log.info(f'Arquivo gerado: {nome_arquivo} - Quantidade de linhas: {qtd_linhas_arquivo}')

    if qtd_linhas_qs == qtd_linhas_arquivo:
        log.info('Inicia Atualização dos registros para: enviado_para_mercado_pago = True')
        for responsavel in qs:
            obj_responsavel = Responsavel.objects.get(codigo_eol_aluno=responsavel.get('codigo_eol_aluno'))
            obj_responsavel.enviado_para_mercado_pago = True
            obj_responsavel.save()

        # TODO: Chamar aqui a funcão de enviar e-mail passando o arquivo por parametro.
    else:
        log.info('Divergencia no número de linhas da query com o número de linhas do arquivo gerado. '
                 'Registros não foram atualizados e e-mail não foi enviado.')
        # TODO: Verificar uma forma de guardar essa informação no banco
