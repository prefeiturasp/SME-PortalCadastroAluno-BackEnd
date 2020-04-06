import logging
import datetime

import environ
import requests
from rest_framework import status

from ..alunos.models import Aluno, Responsavel
from ..alunos.models.log_consulta_eol import LogConsultaEOL
from ..alunos.api.services.aluno_service import AlunoService
from .helpers import ajusta_cpf
from ..core.constants import ESCOLAS_CEI

env = environ.Env()
DJANGO_EOL_API_TOKEN = env('DJANGO_EOL_API_TOKEN')
DJANGO_EOL_API_URL = env('DJANGO_EOL_API_URL')
DJANGO_EOL_API_ATUALIZAR_URL = env('DJANGO_EOL_API_ATUALIZAR_URL')
USUARIO_EOL_API = env('DJANGO_EOL_API_USER')
SENHA_EOL_API = env('DJANGO_EOL_API_PASSWORD')
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
    DEFAULT_AUTH = ({USUARIO_EOL_API}, {SENHA_EOL_API})
    DEFAULT_HEADERS = {'Authorization': f'Token {DJANGO_EOL_API_TOKEN}'}
    DEFAULT_HEADERS_TERC = {'Authorization': f'Token {DJANGO_EOL_API_TERC_TOKEN}'}
    DEFAULT_TIMEOUT = 20

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
    def get_alunos_escola(cls, cod_eol_escola):
        log.info(f"Buscando alunos de uma escola com o código EOL: {cod_eol_escola}")
        response = requests.get(f'{DJANGO_EOL_API_TERC_URL}/escola_turma_aluno/{cod_eol_escola}',
                                headers=cls.DEFAULT_HEADERS_TERC,
                                timeout=cls.DEFAULT_TIMEOUT)
        if response.status_code == status.HTTP_200_OK:
            results = response.json()['results']
            log.info(f"Alunos da escola: {results}")
            if len(results) >= 1:
                if cod_eol_escola in ESCOLAS_CEI:
                    results = [aluno for aluno in results if
                               aluno.get('dc_serie_ensino') in ['INFANTIL I', 'INFANTIL II']]
                return results
            raise EOLException(f'Resultados para o Código EOL: {cod_eol_escola} vazios')
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
        if not dados['responsaveis']:
            raise EOLException('Código com cadastro incompleto. Falta cadastrar no EOL o(a) responsável ' +
                               'pela criança, para depois fazer a solicitação do uniforme')
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

    @classmethod
    def atualizar_dados_responsavel(cls, codigo_eol: str, vinculo: str, nome: str, cpf: str, ddd_celular: str,
                                    celular: str, email: str, nome_mae: str, data_nascimento: str):
        payload = {
            "usuario": "webResp",
            "senha": "resp",
            "cd_aluno": codigo_eol,
            "tp_pessoa_responsavel": vinculo,
            "nm_responsavel": nome,
            "cpf": cpf,
            "cd_ddd_celular_responsavel": ddd_celular,
            "nr_celular_responsavel": celular,
            "in_autoriza_envio_sms_responsavel": "S",
            "email_responsavel": email,
            "nm_mae_responsavel": nome_mae,
            "dt_nascimento_responsavel": data_nascimento,
            "nr_rg_responsavel": None,
            "cd_digito_rg_responsavel": None,
            "sg_uf_rg_responsavel": None,
            "in_cpf_responsavel_confere": None,
            "cd_tipo_turno_celular": None,
            "cd_ddd_telefone_fixo_responsavel": None,
            "nr_telefone_fixo_responsavel": None,
            "cd_tipo_turno_fixo": None,
            "cd_ddd_telefone_comercial_responsavel": None,
            "nr_telefone_comercial_responsavel": None,
            "cd_tipo_turno_comercial": None,
        }

        response = requests.post({DJANGO_EOL_API_ATUALIZAR_URL},
                                 auth=cls.DEFAULT_AUTH,
                                 timeout=cls.DEFAULT_TIMEOUT,
                                 data=payload)

        return response
