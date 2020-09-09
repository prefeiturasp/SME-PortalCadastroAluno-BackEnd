from rest_framework import serializers

from sme_portal_aluno_apps.eol_servico.utils import EOLService
from ...models import Responsavel, validators


class ResponsavelSerializer(serializers.ModelSerializer):
    nm_responsavel = serializers.CharField(source='nome')
    tp_pessoa_responsavel = serializers.CharField(source='vinculo')
    cd_cpf_responsavel = serializers.CharField(source='cpf', validators=[validators.cpf_validation])
    cd_ddd_celular_responsavel = serializers.CharField(source='ddd_celular', required=False, allow_null=True)
    nr_celular_responsavel = serializers.CharField(source='celular', validators=[validators.phone_validation],
                                                   required=False, allow_null=True)
    email_responsavel = serializers.CharField(source='email', validators=[validators.email_validation], required=False,
                                              allow_null=True)

    class Meta:
        model = Responsavel
        fields = ('codigo_eol_aluno', 'nm_responsavel', 'cd_cpf_responsavel', 'cd_ddd_celular_responsavel',
                  'nr_celular_responsavel', 'email_responsavel', 'tp_pessoa_responsavel', 'nome_mae',
                  'data_nascimento', 'status', 'nao_possui_celular', 'nao_possui_email', 'enviado_para_mercado_pago')


class ResponsavelSerializerComCPFEOL(serializers.ModelSerializer):
    nm_responsavel = serializers.CharField(source='nome')
    tp_pessoa_responsavel = serializers.CharField(source='vinculo')
    cd_cpf_responsavel = serializers.CharField(source='cpf', validators=[validators.cpf_validation])
    cd_ddd_celular_responsavel = serializers.CharField(source='ddd_celular', required=False, allow_null=True)
    nr_celular_responsavel = serializers.CharField(source='celular', validators=[validators.phone_validation],
                                                   required=False, allow_null=True)
    email_responsavel = serializers.CharField(source='email', validators=[validators.email_validation], required=False,
                                              allow_null=True)
    cpf_eol = serializers.SerializerMethodField()

    def get_cpf_eol(self, obj):
        return EOLService.get_cpf_eol_responsavel(obj.codigo_eol_aluno)

    class Meta:
        model = Responsavel
        fields = ('codigo_eol_aluno', 'nm_responsavel', 'cd_cpf_responsavel', 'cd_ddd_celular_responsavel',
                  'nr_celular_responsavel', 'email_responsavel', 'tp_pessoa_responsavel', 'nome_mae',
                  'data_nascimento', 'status', 'cpf_eol', 'nao_possui_celular', 'nao_possui_email',
                  'enviado_para_mercado_pago')


class ResponsavelListSerializer(serializers.ModelSerializer):
    codigo_eol = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_codigo_eol(self, obj):
        return obj.alunos.codigo_eol

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Responsavel
        fields = ('nome', 'cpf', 'codigo_eol', 'status')


class ResponsavelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responsavel
        exclude = ('id', 'responsavel')
