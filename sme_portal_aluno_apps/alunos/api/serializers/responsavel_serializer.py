from rest_framework import serializers
from ...models import Responsavel, validators


class ResponsavelSerializer(serializers.ModelSerializer):
    nm_responsavel = serializers.CharField(source='nome')
    tp_pessoa_responsavel = serializers.CharField(source='vinculo')
    cd_cpf_responsavel = serializers.CharField(source='cpf', validators=[validators.cpf_validation])
    cd_ddd_celular_responsavel = serializers.CharField(source='ddd_celular')
    nr_celular_responsavel = serializers.CharField(source='celular', validators=[validators.phone_validation])
    email_responsavel = serializers.CharField(source='email', validators=[validators.email_validation])

    class Meta:
        model = Responsavel
        fields = ('nm_responsavel', 'cd_cpf_responsavel', 'cd_ddd_celular_responsavel', 'nr_celular_responsavel',
                  'email_responsavel', 'tp_pessoa_responsavel', 'nome_mae', 'data_nascimento', 'status')


class ResponsavelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Responsavel
        exclude = ('id', 'responsavel')
