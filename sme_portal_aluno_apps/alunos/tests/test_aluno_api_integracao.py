import json

import pytest
from rest_framework import status
from .conftest import mocked_request_api_eol
from ..api.serializers.aluno_serializer import AlunoCreateSerializer

pytestmark = pytest.mark.django_db


def test_aluno_api_retrieve(client_logado, aluno):
    response = client_logado.get(f'/alunos/{aluno.codigo_eol}/')
    assert response.status_code == status.HTTP_200_OK
    assert str(aluno.codigo_eol) in response.content.decode("utf-8")


def test_aluno_api_create_or_update(client_logado, payload, monkeypatch):
    monkeypatch.setattr(AlunoCreateSerializer, 'atualiza_payload',
                        lambda p1, p2: mocked_request_api_eol())
    response = client_logado.post('/alunos/', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED


