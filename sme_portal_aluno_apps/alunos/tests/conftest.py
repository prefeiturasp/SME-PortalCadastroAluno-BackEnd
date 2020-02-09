import pytest
from model_bakery import baker


@pytest.fixture
def responsavel():
    return baker.make(
        'Responsavel',
        nome='Fulano',
        vinculo='Pai',
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
        responsavel=responsavel
    )


@pytest.fixture
def payload_alunos():
    return [
        {
            "codigo_eol": "6219731",
            "data_nascimento": "2014-04-13"
        }
    ]



@pytest.fixture
def payload_responsavel(payload_alunos):
    return {
        "alunos": payload_alunos,
        "vinculo": "RESPONSAVEL_LEGAL",
        "nome": "João Ninguém",
        "cpf": "13381973720",
        "email": "jn@gmail.com",
        "ddd_celular": "27",
        "celular": "998391003",
        "data_nascimento": "1992-02-08",
        "nome_mae": "Mãe Jão",
        "status": "PENDENTE"
    }
