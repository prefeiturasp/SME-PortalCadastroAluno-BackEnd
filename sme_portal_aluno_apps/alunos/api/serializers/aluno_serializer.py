from rest_framework import serializers

from ...models import Aluno


class AlunoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aluno
        fields = ('uuid', 'codigo_eol', 'data_nascimento', 'responsavel', 'criado_em')


class AlunoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aluno
        exclude = ('id', 'responsavel')
