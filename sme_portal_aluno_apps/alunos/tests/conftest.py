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
        data_nascimento='2014-06-12',
        nome_mae='Mãe Fulano'
    )


@pytest.fixture
def aluno(responsavel):
    return baker.make(
        'Aluno',
        codigo_eol='005294',
        responsavel=responsavel
    )
