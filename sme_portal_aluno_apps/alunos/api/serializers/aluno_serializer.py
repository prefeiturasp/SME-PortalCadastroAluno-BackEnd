from rest_framework import serializers

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
    responsavel = ResponsavelSerializer()

    def create(self, validated_data):
        responsavel = validated_data.pop('responsavel')
        try:
            responsavel = Responsavel.objects.get(cpf=responsavel['cpf'])
        except Responsavel.DoesNotExist:
            responsavel = Responsavel.objects.create(**responsavel)
        # responsavel, created = Responsavel.objects.update_or_create(**responsavel)
        # codigo_eol = validated_data.pop('codigo_eol')
        # validated_data['responsavel'] = responsavel
        print(validated_data)
        try:
            aluno = Aluno.objects.get(codigo_eol=validated_data['codigo_eol'])
        except Aluno.DoesNotExist:
            aluno = Aluno.objects.create(**validated_data, responsavel=responsavel)

        # aluno, created = Aluno.objects.update_or_create(codigo_eol=codigo_eol,
        #                                        defaults={
        #                                            'data_nascimento': validated_data.get('data_nascimento'),
        #                                            'responsavel': validated_data.get('responsavel', None),
        #                                        })
        # aluno, created = Aluno.objects.update_or_create(codigo_eol=codigo_eol,
        #                                                 defaults={
        #                                                     'data_nascimento': validated_data.get('data_nascimento'),
        #                                                     'responsavel': validated_data.get('responsavel'),
        #                                                 })

        return aluno

    class Meta:
        model = Aluno
        exclude = ('id',)
