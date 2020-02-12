from copy import copy

from rest_framework import serializers, validators

from ...models import Aluno, Responsavel
from ...api.serializers.responsavel_serializer import ResponsavelSerializer


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
            a = Responsavel.objects.get(cpf=responsavel['cpf'])
            if a:
                cpf = responsavel.pop('cpf')
                resp, created = Responsavel.objects.update_or_create(
                    cpf = cpf,
                    defaults={**responsavel})
                print('resp ', resp)
                print('responsavel ', responsavel)
        except Responsavel.DoesNotExist:
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
