import logging
from rest_framework.response import Response
from rest_framework import serializers, status

from ...models import Aluno, Responsavel
from ...api.serializers.responsavel_serializer import ResponsavelSerializer
from sme_portal_aluno_apps.eol_servico.utils import EOLService, EOLException

log = logging.getLogger(__name__)


class AlunoSerializer(serializers.ModelSerializer):
    responsaveis = ResponsavelSerializer(source='responsavel')
    codigo_eol = serializers.CharField(read_only=True)

    class Meta:
        model = Aluno
        fields = ('uuid', 'codigo_eol', 'nome', 'data_nascimento', 'codigo_escola', 'codigo_dre',
                  'criado_em', 'responsaveis')


class AlunoLookUpSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')
    responsavel_nome = serializers.SerializerMethodField()

    def get_responsavel_nome(self, obj):
        return obj.responsavel.nome

    def get_status(self, obj):
        return obj.responsavel.get_status_display()

    class Meta:
        model = Aluno
        fields = ('codigo_eol', 'nome', 'data_nascimento', 'status', 'responsavel_nome')


class AlunoCreateSerializer(serializers.ModelSerializer):
    codigo_eol = serializers.CharField()
    responsavel = ResponsavelSerializer()

    def create(self, validated_data):
        log.info(f"Criando Aluno com códio eol: {validated_data.get('codigo_eol')}")
        try:
            informacoes_aluno = EOLService.get_informacoes_responsavel(validated_data['codigo_eol'])
        except EOLException as e:
            log.info(f"Erro ao buscar informações do aluno: {e}")
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

        responsavel = validated_data.pop('responsavel')
        try:
            obj_aluno = Aluno.objects.get(codigo_eol=validated_data['codigo_eol'])
            if obj_aluno:
                cpf = responsavel['cpf']
                if EOLService.cpf_divergente(validated_data['codigo_eol'], cpf):
                    responsavel['status'] = 'DIVERGENTE'
                else:
                    responsavel['status'] = 'ATUALIZADO_VALIDO'
                resp, created = Responsavel.objects.update_or_create(
                    codigo_eol_aluno=validated_data['codigo_eol'],
                    defaults={**responsavel})
                if informacoes_aluno:
                    validated_data['nome'] = informacoes_aluno['nome']
                    validated_data['codigo_escola'] = informacoes_aluno['codigo_escola']
                    validated_data['codigo_dre'] = informacoes_aluno['codigo_dre']
                log.info(f"Aluno existe. Eol: {validated_data['codigo_eol']}, nome responsavel: {resp.nome}")
        except Aluno.DoesNotExist:
            if EOLService.cpf_divergente(validated_data['codigo_eol'], responsavel['cpf']):
                responsavel['status'] = 'DIVERGENTE'
            if informacoes_aluno:
                validated_data['nome'] = informacoes_aluno['nm_aluno']
                validated_data['codigo_escola'] = informacoes_aluno['cd_escola']
                validated_data['codigo_dre'] = informacoes_aluno['cd_dre']
            resp, created = Responsavel.objects.update_or_create(**responsavel)
            log.info(f"Aluno não existe. Eol: {validated_data['codigo_eol']}, nome responsavel: {resp.nome}")

        codigo = validated_data.pop('codigo_eol')
        validated_data['responsavel'] = resp
        aluno, created = Aluno.objects.update_or_create(codigo_eol=codigo,
                                                        defaults={
                                                            **validated_data
                                                        })
        log.info("Aluno Criado.")
        resp.enviar_email_confirmacao()
        return aluno

    class Meta:
        model = Aluno
        exclude = ('id',)
