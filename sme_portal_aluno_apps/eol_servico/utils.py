import logging
import datetime

import environ
import requests
from rest_framework import status

from ..alunos.models import Aluno, Responsavel
from ..alunos.models.log_consulta_eol import LogConsultaEOL
from ..alunos.api.services.aluno_service import AlunoService
from .helpers import ajusta_cpf

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
    DEFAULT_TIMEOUT = 10

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
    def get_cpf_eol_responsavel(cls, codigo_eol):
        log.info(f"Buscando CPF do responsável do eol: {codigo_eol}")
        response = requests.get(f'{DJANGO_EOL_API_URL}/responsaveis/{codigo_eol}',
                                headers=cls.DEFAULT_HEADERS,
                                timeout=cls.DEFAULT_TIMEOUT)
        if response.status_code == status.HTTP_200_OK:
            results = response.json()['results']
            if len(results) == 1:
                return ajusta_cpf(results[0].get('responsaveis')[0].get('cd_cpf_responsavel'))
            raise EOLException(f'Resultados para o código: {codigo_eol} vazios')
        else:
            raise EOLException(f'Código EOL não existe')

    @classmethod
    def registra_log(cls, codigo_eol, json):
        LogConsultaEOL.objects.create(codigo_eol=codigo_eol, json=json)

    @classmethod
    def get_informacoes_usuario(cls, registro_funcional):
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
        cpf_eol = ''
        response = requests.get(f'{DJANGO_EOL_API_URL}/responsaveis/{codigo_eol}',
                                headers=cls.DEFAULT_HEADERS,
                                timeout=cls.DEFAULT_TIMEOUT)
        if response.status_code == status.HTTP_200_OK:
            results = response.json()['results']
            if results and results[0]['responsaveis']:
                cpf_eol = ajusta_cpf(results[0]['responsaveis'][0].pop('cd_cpf_responsavel'))
            return cpf != cpf_eol

    @classmethod
    def cria_aluno_desatualizado(cls, codigo_eol):
        dados = cls.get_informacoes_responsavel(codigo_eol)
        cls.registra_log(codigo_eol, dados)
        cpf = ajusta_cpf(dados['responsaveis'][0]['cd_cpf_responsavel'])
        data_nascimento = datetime.datetime.strptime(dados['dt_nascimento_aluno'], "%Y-%m-%dT%H:%M:%S")
        responsavel = Responsavel.objects.create(
            vinculo=dados['responsaveis'][0]['tp_pessoa_responsavel'],
            codigo_eol_aluno=codigo_eol,
            nome=dados['responsaveis'][0]['nm_responsavel'].strip() if dados['responsaveis'][0][
                'nm_responsavel'] else None,
            cpf=cpf,
            ddd_celular=dados['responsaveis'][0]['cd_ddd_celular_responsavel'].strip() if dados['responsaveis'][0][
                'cd_ddd_celular_responsavel'] else None,
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
