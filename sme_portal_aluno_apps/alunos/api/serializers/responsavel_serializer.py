from rest_framework import serializers

from ...models import Responsavel


class ResponsavelSerializer(serializers.ModelSerializer):
    nm_responsavel = serializers.CharField(source='nome')
    dc_tipo_responsavel = serializers.CharField(source='vinculo')
    cd_cpf_responsavel = serializers.CharField(source='cpf')
    cd_ddd_celular_responsavel = serializers.CharField(source='ddd_celular')
    nr_celular_responsavel = serializers.CharField(source='celular')
    email_responsavel = serializers.CharField(source='email')

    class Meta:
        model = Responsavel
        fields = ('nm_responsavel', 'cd_cpf_responsavel', 'cd_ddd_celular_responsavel', 'nr_celular_responsavel',
                  'email_responsavel', 'dc_tipo_responsavel', 'nome_mae', 'data_nascimento')


class ResponsavelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Responsavel
        exclude = ('id', 'responsavel')
