from rest_framework import serializers

from ...models import Responsavel
from ...api.serializers.aluno_serializer import AlunoSerializer, AlunoCreateSerializer


class ResponsavelSerializer(serializers.ModelSerializer):
    # alunos = AlunoSerializer(many=True)

    class Meta:
        model = Responsavel
        fields = '__all__'


class ResponsavelLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        fields = ('uuid', 'nome', 'cpf', 'vinculo', 'status', 'criado_em', 'alterado_em')


class ResponsavelCreateSerializer(serializers.ModelSerializer):
    alunos = AlunoSerializer(many=True)

    def create(self, validated_data):
        alunos = validated_data.pop('alunos')
        try:
            responsavel = Responsavel.objects.get(cpf=validated_data['cpf'])
        except Responsavel.DoesNotExist:
            responsavel = Responsavel.objects.create(**validated_data)

        alunos_lista = []
        for aluno in alunos:
            aluno_object = AlunoCreateSerializer().create(aluno)
            alunos_lista.append(aluno_object)
        responsavel.alunos.set(alunos_lista)

        return responsavel

    class Meta:
        model = Responsavel
        exclude = ('id',)
