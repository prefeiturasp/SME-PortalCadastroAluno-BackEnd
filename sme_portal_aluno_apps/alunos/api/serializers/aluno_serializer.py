from copy import copy

from rest_framework import serializers, validators

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

    def run_validators(self, value):
        for validator in copy(self.validators):
            if isinstance(validator, validators.UniqueValidator):
                self.validators.remove(validator)
        super(AlunoCreateSerializer, self).run_validators(value)

    def create(self, validated_data):
        responsavel = validated_data.pop('responsavel')
        try:
            obj = Responsavel.objects.get(cpf=responsavel['cpf'])
            if obj:
                cpf = responsavel.pop('cpf')
                if EOL.cpf_divergente(validated_data['codigo_eol'], cpf):
                    responsavel['status'] = 'DIVERGENTE'
                resp, created = Responsavel.objects.update_or_create(
                    cpf=cpf,
                    defaults={**responsavel})
        except Responsavel.DoesNotExist:
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
