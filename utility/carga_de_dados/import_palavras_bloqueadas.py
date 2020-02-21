import csv
import environ
from sme_portal_aluno_apps.core.models import ListaPalavrasBloqueadas
ROOT_DIR = environ.Path(__file__) - 1


def cria_palavra_bloqueada(palavra):
    return ListaPalavrasBloqueadas.objects.create(palavra=palavra)


class PalavraBloqueada(object):

    @classmethod
    def importa_palavras_bloqueadas(cls):
        with open(f'{ROOT_DIR}/lista_palavras_bloqueadas.csv', 'r') as file:
            lista_palavras = csv.reader(file, delimiter="'")
            for palavra in lista_palavras:
                cria_palavra_bloqueada(palavra[0])
