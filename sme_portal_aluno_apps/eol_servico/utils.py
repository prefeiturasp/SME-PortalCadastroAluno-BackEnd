import environ
import requests
from rest_framework import status

from ..alunos.models import Aluno
from ..alunos.models.log_consulta_eol import LogConsultaEOL
from ..alunos.api.serializers.aluno_serializer import AlunoSerializer

env = environ.Env()
DJANGO_EOL_API_TOKEN = env('DJANGO_EOL_API_TOKEN')
DJANGO_EOL_API_URL = env('DJANGO_EOL_API_URL')
DJANGO_EOL_API_TERC_TOKEN = env('DJANGO_EOL_API_TERC_TOKEN')
DJANGO_EOL_API_TERC_URL = env('DJANGO_EOL_API_TERC_URL')


def aluno_existe(codigo_eol):
    try:
        Aluno.objects.get(codigo_eol=codigo_eol)
        return True
    except Aluno.DoesNotExist:
        return False


class EOLException(Exception):
    pass


class EOLService(object):
    DEFAULT_HEADERS = {'Authorization': f'Token {DJANGO_EOL_API_TOKEN}'}
    DEFAULT_HEADERS_TERC = {'Authorization': f'Token {DJANGO_EOL_API_TERC_TOKEN}'}
    DEFAULT_TIMEOUT = 5

    @classmethod
    def get_informacoes_responsavel(cls, codigo_eol):
        if aluno_existe(codigo_eol):
            aluno = Aluno.objects.get(codigo_eol=codigo_eol)
            response = AlunoSerializer(aluno).data
            responsaveis = [response['responsaveis']]
            response['responsaveis'] = responsaveis
            return response
        else:
            response = requests.get(f'{DJANGO_EOL_API_URL}/responsaveis/{codigo_eol}',
                                    headers=cls.DEFAULT_HEADERS,
                                    timeout=cls.DEFAULT_TIMEOUT)
            if response.status_code == status.HTTP_200_OK:
                results = response.json()['results']
                if len(results) == 1:
                    return results[0]
                raise EOLException(f'Resultados para o código: {codigo_eol} vazios')
            else:
                raise EOLException(f'API EOL com erro. Status: {response.status_code}')

    @classmethod
    def registra_log(cls, codigo_eol, json):
        LogConsultaEOL.objects.create(codigo_eol=codigo_eol, json=json)

    @classmethod
    def get_informacoes_usuario(cls, registro_funcional):
        """Retorna detalhes de vínculo de um RF.

        mostra todos os vínculos desse RF. EX: fulano é diretor em AAAA e ciclano é professor em BBBB.
            {
        "results": [
            {
                "nm_pessoa": "XXXXXXXX",
                "cd_cpf_pessoa": "000.000.000-00",
                "cargo": "ANALISTA DE SAUDE NIVEL I",
                "divisao": "NUCLEO DE SUPERVISAO DA ALIMENT ESCOLAR - CODAE-DINUTRE-NSAE",
                "coord": null
            }
            ]
            }
        """
        print(cls.DEFAULT_HEADERS_TERC)
        print(DJANGO_EOL_API_TERC_URL)
        response = requests.get(f'{DJANGO_EOL_API_TERC_URL}/cargos/{registro_funcional}',
                                headers=cls.DEFAULT_HEADERS_TERC,
                                timeout=cls.DEFAULT_TIMEOUT)
        if response.status_code == status.HTTP_200_OK:
            results = response.json()['results']
            if len(results) >= 1:
                return results
            raise EOLException(f'Resultados para o RF: {registro_funcional} vazios')
        else:
            raise EOLException(f'API EOL com erro. Status: {response.status_code}')
