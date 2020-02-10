import environ
import requests
from rest_framework import status

from rest_framework.response import Response
from ..alunos.models import Aluno, Responsavel
from ..alunos.models.log_consulta_eol import LogConsultaEOL
from ..alunos.api.serializers.responsavel_serializer import ResponsavelSerializer

env = environ.Env()
DJANGO_EOL_API_TOKEN = env('DJANGO_EOL_API_TOKEN')
DJANGO_EOL_API_URL = env('DJANGO_EOL_API_URL')


def aluno_existe(codigo_eol):
    try:
        aluno = Aluno.objects.get(codigo_eol=codigo_eol)
        return True
    except Aluno.DoesNotExist:
        return False


class EOLException(Exception):
    pass


class EOLService(object):
    DEFAULT_HEADERS = {'Authorization': f'Token {DJANGO_EOL_API_TOKEN}'}
    DEFAULT_TIMEOUT = 5

    @classmethod
    def get_informacoes_responsavel(cls, codigo_eol):
        if aluno_existe(codigo_eol):
            responsavel = Responsavel.objects.get(alunos__codigo_eol=codigo_eol)
            response = ResponsavelSerializer(responsavel).data
            return response
        else:
            response = requests.get(f'{DJANGO_EOL_API_URL}/responsaveis/{codigo_eol}',
                                    headers=cls.DEFAULT_HEADERS,
                                    timeout=cls.DEFAULT_TIMEOUT)
            # print(response)
            if response.status_code == status.HTTP_200_OK:
                results = response.json()['results']
                # print(results)
                if len(results) == 1:
                    # print(results[0])
                    return results[0]
                raise EOLException(f'Resultados para o código: {codigo_eol} vazios')
            else:
                raise EOLException(f'API EOL com erro. Status: {response.status_code}')

    @classmethod
    def registra_log(cls, codigo_eol, json):
        LogConsultaEOL.objects.create(codigo_eol=codigo_eol, json=json)
