import json

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_aluno_api_retrieve(client, aluno):
    response = client.get(f'/alunos/{aluno.codigo_eol}/')
    assert response.status_code == status.HTTP_200_OK
    assert str(aluno.codigo_eol) in response.content.decode("utf-8")


def test_aluno_api_create_or_update(client, payload):
    response = client.post('/alunos/', data=json.dumps(payload), content_type='application/json')

    assert response.status_code == status.HTTP_201_CREATED


