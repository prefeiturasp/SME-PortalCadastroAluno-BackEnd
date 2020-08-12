from os.path import join

from ..models.responsavel import Responsavel
from config.settings.base import MEDIA_ROOT
from djqscsv import write_csv, render_to_csv_response


def gerar_csv():
    qs = Responsavel.objects.filter(status=Responsavel.STATUS_ATUALIZADO_EOL, enviado_para_mercado_pago=False).values(
        'nome', 'cpf', 'codigo_eol_aluno', 'alunos__nome'
    )
    # return render_to_csv_response(qs)
    path = join(MEDIA_ROOT, 'teste-mp.csv')
    with open(path, 'wb') as csv_file:
        write_csv(qs, csv_file)
