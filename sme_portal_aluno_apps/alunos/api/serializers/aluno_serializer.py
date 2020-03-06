import logging

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import serializers, status

from .responsavel_serializer import ResponsavelSerializerComCPFEOL
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


class AlunoSerializerComCPFEol(serializers.ModelSerializer):
    responsaveis = ResponsavelSerializerComCPFEOL(source='responsavel')
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

    def get_status(self, codigo_eol, cpf, atualizado_na_escola):
        if EOLService.cpf_divergente(codigo_eol, cpf) and atualizado_na_escola:
            return 'PENDENCIA_RESOLVIDA'
        elif EOLService.cpf_divergente(codigo_eol, cpf):
            return 'DIVERGENTE'
        elif atualizado_na_escola:
            return 'ATUALIZADO_VALIDO'
        else:
            return 'ATUALIZADO_VALIDO'

    def atualiza_payload(self, validated_data):
        try:
            informacoes_aluno = EOLService.get_informacoes_responsavel(validated_data['codigo_eol'])
            validated_data['nome'] = informacoes_aluno.get('nome') or informacoes_aluno.get('nm_aluno')
            validated_data['codigo_escola'] = informacoes_aluno.get('codigo_escola') or informacoes_aluno.get('cd_escola')
            validated_data['codigo_dre'] = informacoes_aluno.get('codigo_dre') or informacoes_aluno.get('cd_dre')
            return validated_data
        except EOLException as e:
            log.info(f"Erro ao buscar informações do aluno: {e}")
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, validated_data):
        atualizado_na_escola = validated_data.get('atualizado_na_escola', False)
        user = self.context['request'].user
        if atualizado_na_escola:
            validated_data['servidor'] = user.username
        log.info(f"Criando Aluno com códio eol: {validated_data.get('codigo_eol')}")
        self.atualiza_payload(validated_data)
        responsavel = validated_data.pop('responsavel')
        cpf = responsavel.get('cpf', None)
        try:
            aluno_obj = Aluno.objects.get(codigo_eol=validated_data['codigo_eol'])
            if aluno_obj.atualizado_na_escola and not user.codigo_escola:
                raise ValidationError('Solicitação finalizada. Não pode atualizar os dados.')
            responsavel['status'] = self.get_status(validated_data['codigo_eol'], cpf, atualizado_na_escola)
            responsavel_criado, created = Responsavel.objects.update_or_create(
                codigo_eol_aluno=validated_data['codigo_eol'], defaults={**responsavel})
            log.info(f"Aluno existe. Eol: {validated_data['codigo_eol']}, nome responsavel: {responsavel_criado.nome}")
        except Aluno.DoesNotExist:
            responsavel['status'] = self.get_status(validated_data['codigo_eol'], cpf, atualizado_na_escola)
            responsavel_criado, created = Responsavel.objects.update_or_create(**responsavel)
            validated_data['responsavel'] = responsavel_criado
            log.info(f"Aluno criado. Eol: {validated_data['codigo_eol']}, nome responsavel: {responsavel_criado.nome}")
        codigo = validated_data.pop('codigo_eol')
        aluno, created = Aluno.objects.update_or_create(codigo_eol=codigo, defaults={**validated_data})
        log.info("Inicia envio de email.")
        responsavel_criado.enviar_email()
        log.info("Aluno Criado/Atualizado.")
        return aluno

    class Meta:
        model = Aluno
        exclude = ('id',)
