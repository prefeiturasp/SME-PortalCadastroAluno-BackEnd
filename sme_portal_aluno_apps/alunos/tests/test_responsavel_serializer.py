import pytest

from ..api.serializers.responsavel_serializer import ResponsavelSerializer, ResponsavelLookUpSerializer

pytestmark = pytest.mark.django_db


def test_responsavel_serializer(responsavel):
    responsavel_serializer = ResponsavelSerializer(responsavel)

    assert responsavel_serializer.data is not None
    assert responsavel_serializer.data['cpf']
    assert responsavel_serializer.data['nome']
    assert responsavel_serializer.data['alterado_em']
    assert responsavel_serializer.data['uuid']
    assert responsavel_serializer.data['data_nascimento']
    assert responsavel_serializer.data['ddd_celular']
    assert responsavel_serializer.data['celular']
    assert responsavel_serializer.data['nome_mae']
    assert responsavel_serializer.data['vinculo']
    assert responsavel_serializer.data['email']
    assert responsavel_serializer.data['criado_em']
    assert responsavel_serializer.data['id']
    assert responsavel_serializer.data['alunos'] is not None


def test_responsavel_lookup_serializer(responsavel):

    responsavel_serializer = ResponsavelLookUpSerializer(responsavel)

    assert responsavel_serializer.data is not None
    assert responsavel_serializer.data['nome']
    assert responsavel_serializer.data['uuid']
    assert responsavel_serializer.data['criado_em']
    assert responsavel_serializer.data['alterado_em']
    assert responsavel_serializer.data['vinculo']
    assert responsavel_serializer.data['status']
    assert responsavel_serializer.data['cpf']
