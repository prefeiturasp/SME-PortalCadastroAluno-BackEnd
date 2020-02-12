import json

import pytest
from rest_framework import status

from ..models.aluno import Aluno

pytestmark = pytest.mark.django_db


def test_aluno_api_retrieve(client, aluno):
    response = client.get(f'/alunos/{aluno.codigo_eol}/')
    assert response.status_code == status.HTTP_200_OK
    assert str(aluno.codigo_eol) in response.content.decode("utf-8")


def test_aluno_api_create(client, payload):
    response = client.post('/alunos/', data=json.dumps(payload), content_type='application/json')

    assert response.status_code == status.HTTP_201_CREATED

#
def test_aluno_api_update(client, aluno, payload):
    payload = {
        "codigo_eol": "6541906",
        "data_nascimento": "2014-05-12",
        "responsavel": {
            "nm_responsavel": "João das Nevesss",
            "cd_cpf_responsavel": "12481973221",
            "cd_ddd_celular_responsavel": "27",
            "nr_celular_responsavel": "998391001",
            "email_responsavel": "teste@gmail.com",
            "dc_tipo_responsavel": "RESPONSAVEL_LEGAL",
            "nome_mae": "Maria das Neves",
            "data_nascimento": "1992-02-08"
        }
    }

    response = client.put(f'/alunos/{aluno.codigo_eol}/', data=json.dumps(payload),
                            content_type='application/json')

    assert response.status_code == status.HTTP_200_OK
