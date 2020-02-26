import logging
import datetime

import environ
import requests
from rest_framework import status

from ..alunos.models import Aluno, Responsavel
from ..alunos.models.log_consulta_eol import LogConsultaEOL
from ..alunos.api.services.aluno_service import AlunoService

env = environ.Env()
DJANGO_EOL_API_TOKEN = env('DJANGO_EOL_API_TOKEN')
DJANGO_EOL_API_URL = env('DJANGO_EOL_API_URL')
DJANGO_EOL_API_TERC_TOKEN = env('DJANGO_EOL_API_TERC_TOKEN')
DJANGO_EOL_API_TERC_URL = env('DJANGO_EOL_API_TERC_URL')

log = logging.getLogger(__name__)


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
        log.info(f"Buscando informações do responsável do eol: {codigo_eol}")
        if aluno_existe(codigo_eol):
            log.info("Informações do aluno já existente na base.")
            return AlunoService.get_aluno_serializer(codigo_eol)
        else:
            log.info('Buscando informações na API EOL.')
            response = requests.get(f'{DJANGO_EOL_API_URL}/responsaveis/{codigo_eol}',
                                    headers=cls.DEFAULT_HEADERS,
                                    timeout=cls.DEFAULT_TIMEOUT)
            if response.status_code == status.HTTP_200_OK:
                results = response.json()['results']
                if len(results) == 1:
                    return results[0]
                raise EOLException(f'Resultados para o código: {codigo_eol} vazios')
            else:
                raise EOLException(f'Código EOL não existe')

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
        log.info(f"Buscando informações do usuário com RF: {registro_funcional}")
        response = requests.get(f'{DJANGO_EOL_API_TERC_URL}/cargos/{registro_funcional}',
                                headers=cls.DEFAULT_HEADERS_TERC,
                                timeout=cls.DEFAULT_TIMEOUT)
        if response.status_code == status.HTTP_200_OK:
            results = response.json()['results']
            log.info(f"Dados usuário: {results}")
            if len(results) >= 1:
                return results
            raise EOLException(f'Resultados para o RF: {registro_funcional} vazios')
        else:
            raise EOLException(f'API EOL com erro. Status: {response.status_code}')

    @classmethod
    def cpf_divergente(cls, codigo_eol, cpf):
        response = requests.get(f'{DJANGO_EOL_API_URL}/responsaveis/{codigo_eol}',
                                headers=cls.DEFAULT_HEADERS,
                                timeout=cls.DEFAULT_TIMEOUT)
        if response.status_code == status.HTTP_200_OK:
            cpf_eol = ''
            results = response.json()['results']
            if results and results[0]['responsaveis']:
                cpf_eol_api = results[0]['responsaveis'][0].pop('cd_cpf_responsavel')
                cpf_eol = str(cpf_eol_api)[:-2]
            return cpf != cpf_eol

    @classmethod
    def cria_aluno_desatualizado(cls, codigo_eol):
        dados = cls.get_informacoes_responsavel(codigo_eol)
        cls.registra_log(codigo_eol, dados)
        data_nascimento = datetime.datetime.strptime(dados['dt_nascimento_aluno'], "%Y-%m-%dT%H:%M:%S")

        responsavel = Responsavel.objects.create(
            vinculo=dados['responsaveis'][0]['tp_pessoa_responsavel'],
            codigo_eol_aluno=codigo_eol,
            nome=dados['responsaveis'][0]['nm_responsavel'].strip(),
            cpf=str(dados['responsaveis'][0]['cd_cpf_responsavel'])[:-2],
            ddd_celular=dados['responsaveis'][0]['cd_ddd_celular_responsavel'].strip(),
            celular=dados['responsaveis'][0]['nr_celular_responsavel'],
            status='DESATUALIZADO'
        )

        aluno = Aluno.objects.create(
            codigo_eol=codigo_eol,
            data_nascimento=data_nascimento,
            nome=dados['nm_aluno'],
            codigo_escola=dados['cd_escola'],
            codigo_dre=dados['cd_dre'],
            responsavel=responsavel,
        )
        return aluno
