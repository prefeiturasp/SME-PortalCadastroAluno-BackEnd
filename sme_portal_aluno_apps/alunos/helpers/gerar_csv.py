from os.path import join
from django.db.models import Value as V
from django.db.models.functions import Concat

from ..models.responsavel import Responsavel
from config.settings.base import MEDIA_ROOT
from djqscsv import write_csv


def gerar_csv_mp():
    qs = Responsavel.objects.annotate(get_celular=Concat('ddd_celular', V(' '), 'celular')).filter(
        status=Responsavel.STATUS_ATUALIZADO_EOL, enviado_para_mercado_pago=False).values(
        'nome', 'alunos__nome', 'codigo_eol_aluno', 'cpf', 'get_celular', 'vinculo', 'data_nascimento',
        'nome_mae', 'status', 'nao_possui_celular', 'nao_possui_email'
    )

    path = join(MEDIA_ROOT, 'pedidos-uniforme.csv')
    with open(path, 'wb') as csv_file:
        write_csv(qs, csv_file,
                  field_header_map={'nome': 'nome_responsavel',
                                    'alunos__nome': 'nome_aluno',
                                    'get_celular': 'celular',
                                    'nome_mae': 'nome_mae_responsavel'
                                    },
                  use_verbose_names=False)
