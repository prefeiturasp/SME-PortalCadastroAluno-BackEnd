from rest_framework import serializers

from ...models import Aluno
# from ...api.serializers.responsavel_serializer import ResponsavelSerializer


class AlunoSerializer(serializers.ModelSerializer):
    # responsaveis = ResponsavelSerializer(many=True)

    class Meta:
        model = Aluno
        fields = ('uuid', 'id', 'codigo_eol', 'data_nascimento', 'responsaveis', 'criado_em', 'alterado_em')


class AlunoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aluno
        # exclude = ('id', 'responsavel')
