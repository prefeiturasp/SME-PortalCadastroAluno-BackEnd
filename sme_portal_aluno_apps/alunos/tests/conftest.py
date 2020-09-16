import pytest
from model_bakery import baker

from sme_portal_aluno_apps.alunos.models import RetornoMP, Responsavel


@pytest.fixture
def client_logado(client, django_user_model, responsavel):
    email = 'test@test.com'
    password = 'bar'
    username = '8888888'
    django_user_model.objects.create_user(password=password, email=email,
                                          username=username)
    client.login(username=username, password=password)
    return client


@pytest.fixture
def responsavel_erro():
    responsavel = baker.make(
        'Responsavel',
        codigo_eol_aluno='3872240',
        nome='Fulano',
        vinculo=2,
        cpf='72641869977',
        email='teste@teste.com',
        ddd_celular='027',
        celular='999999999',
        data_nascimento='2014-06-12',
        nome_mae='Mãe Fulano',
        status='CPF_INVALIDO'
    )
    baker.make(
        'Aluno',
        codigo_eol='3872240',
        responsavel=responsavel
    )
    baker.make('RetornoMP',
               responsavel=responsavel,
               status=RetornoMP.STATUS_CPF_INVALIDO,
               mensagem='CPF inválido',
               cpf='72641869977',
               codigo_eol='3872240',
               data_ocorrencia='2020-09-14')
    return responsavel


@pytest.fixture
def payload_responsavel_erro():
    return {
        "codigo_eol": "3872240",
        "data_nascimento": "2005-07-27",
        "nome": "João Junior",
        "codigo_escola": "123654",
        "codigo_dre": "741258",
        "inconsistencia_resolvida": True,
        "responsavel": {
            "codigo_eol_aluno": "3872240",
            "nm_responsavel": "Mãe Fulano",
            "cd_cpf_responsavel": "72641869977",
            "cd_ddd_celular_responsavel": "27",
            "nr_celular_responsavel": "998391001",
            "email_responsavel": "teste@gmail.com",
            "tp_pessoa_responsavel": 2,
            "nome_mae": "Maria das Neves",
            "data_nascimento": "1992-02-08"
        }
    }



@pytest.fixture
def client_logado_responsavel_erro(client, django_user_model, responsavel_erro):
    email = 'test@test.com'
    password = 'bar'
    username = '8888888'
    django_user_model.objects.create_user(password=password, email=email,
                                          username=username)
    client.login(username=username, password=password)
    return client


@pytest.fixture
def responsavel():
    return baker.make(
        'Responsavel',
        codigo_eol_aluno='3872240',
        nome='Fulano',
        vinculo=2,
        cpf='72641869977',
        email='teste@teste.com',
        ddd_celular='027',
        celular='999999999',
        data_nascimento='2014-06-12',
        nome_mae='Mãe Fulano'
    )


@pytest.fixture
def aluno(responsavel):
    return baker.make(
        'Aluno',
        codigo_eol='3872240',
        data_nascimento='2010-06-12',
        nome='Rafael Aluno da Silva',
        codigo_escola='123456',
        codigo_dre='654321',
        atualizado_na_escola=True,
        servidor='147852',
        responsavel=responsavel
    )


@pytest.fixture
def retorno(responsavel):
    return baker.make(
        'RetornoMP',
        codigo_eol='3872240',
        cpf='00000000000',
        mensagem='Texto explicativo ao usuário sobre o erro',
        data_ocorrencia='2010-06-12',
        status=5,
        responsavel=responsavel
    )


@pytest.fixture
def payload():
    return {
        "codigo_eol": "3872240",
        "data_nascimento": "2005-07-27",
        "nome": "João Junior",
        "codigo_escola": "123654",
        "codigo_dre": "741258",
        "responsavel": {
            "codigo_eol_aluno": "3872240",
            "nm_responsavel": "João das Neves",
            "cd_cpf_responsavel": "12481973221",
            "cd_ddd_celular_responsavel": "27",
            "nr_celular_responsavel": "998391001",
            "email_responsavel": "teste@gmail.com",
            "tp_pessoa_responsavel": 2,
            "nome_mae": "Maria das Neves",
            "data_nascimento": "1992-02-08"
        }
    }


@pytest.fixture
def payload_alunos():
    return [
        {
            "codigo_eol": "6219731",
            "data_nascimento": "2014-04-13"
        }
    ]


def mocked_request_api_eol():
    return {
        "nome": "YASMIN LEITE DOS SANTOS SIMOES",
        "codigo_escola": "094277",
        "codigo_dre": "108400",
    }


@pytest.fixture
def payload_retorno_mp():
    return {
        "codigo_eol": "3872240",
        "cpf": "72641869977",
        "status": 5,
        "mensagem": "texto msg",
        "data_ocorrencia": "2016-02-11"
    }
