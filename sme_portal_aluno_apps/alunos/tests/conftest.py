import pytest
from model_bakery import baker


@pytest.fixture
def client_logado(client, django_user_model):
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
        codigo_eol='005294',
        data_nascimento='2010-06-12',
        nome='Rafael Aluno da Silva',
        codigo_escola='123456',
        codigo_dre='654321',
        atualizado_na_escola=True,
        servidor='147852',
        responsavel=responsavel
    )


@pytest.fixture
def payload():
    return {
        "codigo_eol": "6541906",
        "data_nascimento": "2014-05-12",
        "nome": "João Junior",
        "codigo_escola": "123654",
        "codigo_dre": "741258",
        "responsavel": {
            "codigo_eol_aluno": "6541906",
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
