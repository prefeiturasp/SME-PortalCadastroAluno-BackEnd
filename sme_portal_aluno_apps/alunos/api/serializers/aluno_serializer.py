from copy import copy

from rest_framework import serializers

from ...models import Aluno, Responsavel
from ...api.serializers.responsavel_serializer import ResponsavelSerializer
from ...utils import EOL


class AlunoSerializer(serializers.ModelSerializer):
    responsaveis = ResponsavelSerializer(source='responsavel')
    codigo_eol = serializers.CharField(read_only=True)

    class Meta:
        model = Aluno
        fields = ('uuid', 'codigo_eol', 'data_nascimento', 'criado_em', 'responsaveis')


class AlunoLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ('uuid', 'codigo_eol', 'data_nascimento', 'criado_em')


class AlunoCreateSerializer(serializers.ModelSerializer):
    codigo_eol = serializers.CharField()
    responsavel = ResponsavelSerializer()

    def create(self, validated_data):
        print((validated_data))
        responsavel = validated_data.pop('responsavel')
        try:
            obj_aluno = Aluno.objects.get(codigo_eol=validated_data['codigo_eol'])
            if obj_aluno:
                cpf = responsavel.pop('cpf')
                if EOL.cpf_divergente(validated_data['codigo_eol'], cpf):
                    responsavel['status'] = 'DIVERGENTE'
                resp, created = Responsavel.objects.update_or_create(
                    codigo_eol_aluno=validated_data['codigo_eol'],
                    defaults={**responsavel})
        except Aluno.DoesNotExist:
            if EOL.cpf_divergente(validated_data['codigo_eol'], responsavel['cpf']):
                responsavel['status'] = 'DIVERGENTE'
            resp, created = Responsavel.objects.update_or_create(**responsavel)
        codigo = validated_data.pop('codigo_eol')
        validated_data['responsavel'] = resp
        aluno, created = Aluno.objects.update_or_create(codigo_eol=codigo,
                                                        defaults={
                                                            **validated_data
                                                        })

        return aluno

    class Meta:
        model = Aluno
        exclude = ('id',)
