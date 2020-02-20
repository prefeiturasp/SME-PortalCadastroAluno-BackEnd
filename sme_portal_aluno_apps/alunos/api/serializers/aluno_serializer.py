from rest_framework.response import Response
from rest_framework import serializers, status

from ...models import Aluno, Responsavel
from ...api.serializers.responsavel_serializer import ResponsavelSerializer
from sme_portal_aluno_apps.eol_servico.utils import EOLService, EOLException


class AlunoSerializer(serializers.ModelSerializer):
    responsaveis = ResponsavelSerializer(source='responsavel')
    codigo_eol = serializers.CharField(read_only=True)

    class Meta:
        model = Aluno
        fields = ('uuid', 'codigo_eol', 'nome', 'data_nascimento', 'criado_em', 'responsaveis')


class AlunoLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ('uuid', 'codigo_eol', 'data_nascimento', 'criado_em')


class AlunoCreateSerializer(serializers.ModelSerializer):
    codigo_eol = serializers.CharField()
    responsavel = ResponsavelSerializer()

    def create(self, validated_data):
        try:
            informacoes_aluno = EOLService.get_informacoes_responsavel(validated_data['codigo_eol'])
        except EOLException as e:
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        if informacoes_aluno:
            validated_data['nome'] = informacoes_aluno['nm_aluno']
            validated_data['codigo_escola'] = informacoes_aluno['cd_escola']
            validated_data['codigo_dre'] = informacoes_aluno['cd_dre']
        responsavel = validated_data.pop('responsavel')
        try:
            obj_aluno = Aluno.objects.get(codigo_eol=validated_data['codigo_eol'])
            if obj_aluno:
                cpf = responsavel.pop('cpf')
                if EOLService.cpf_divergente(validated_data['codigo_eol'], cpf):
                    responsavel['status'] = 'DIVERGENTE'
                resp, created = Responsavel.objects.update_or_create(
                    codigo_eol_aluno=validated_data['codigo_eol'],
                    defaults={**responsavel})
        except Aluno.DoesNotExist:
            if EOLService.cpf_divergente(validated_data['codigo_eol'], responsavel['cpf']):
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
