import json

import pytest
from rest_framework import status

from ..models.responsavel import Responsavel

pytestmark = pytest.mark.django_db


def test_responsavel_api_retrieve(client, responsavel):
    response = client.get(f'/responsaveis/{responsavel.uuid}/')
    assert response.status_code == status.HTTP_200_OK
    assert str(responsavel.uuid) in response.content.decode("utf-8")


def test_responsavel_api_create(client, payload_responsavel):
    response = client.post('/responsaveis/', data=json.dumps(payload_responsavel), content_type='application/json')
    result = json.loads(response.content)

    assert response.status_code == status.HTTP_201_CREATED
    assert Responsavel.objects.get(uuid=result["uuid"]).alunos.all().count() == 1


def test_responsavel_api_update(client, responsavel):
    payload = {
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

    assert Responsavel.objects.get(uuid=responsavel.uuid).alunos.all().count() == 0

    response = client.patch(f'/responsaveis/{responsavel.uuid}/', data=json.dumps(payload),
                            content_type='application/json')

    assert response.status_code == status.HTTP_200_OK
