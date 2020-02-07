from rest_framework import serializers

from .responsavel_serializer import ResponsavelSerializer
from ...models import Aluno


class AlunoSerializer(serializers.ModelSerializer):
    responsavel = serializers.SerializerMethodField()

    class Meta:
        model = Aluno
        fields = '__all__'

    def get_responsavel(self, instance):
        responsavel = instance.responsavel.all().order_by('id')
        return ResponsavelSerializer(responsavel, many=True).data


class AlunoLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ('uuid', 'codigo_eol', 'criado_em')


class AlunoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aluno
        exclude = ('id', 'responsavel')
