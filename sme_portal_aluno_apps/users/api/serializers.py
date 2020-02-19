from rest_framework import serializers

from sme_portal_aluno_apps.eol_servico.utils import EOLService
from sme_portal_aluno_apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    def get_informacoes_usuario(self, validated_data):
        return EOLService.get_informacoes_usuario(validated_data['username'])

    def create(self, validated_data):  # noqa C901
        informacoes_usuario_json = self.get_informacoes_usuario(validated_data)
        cpf = informacoes_usuario_json[0]['cd_cpf_pessoa']
        email = f'{validated_data["email"]}'  # @sme.prefeitura.sp.gov.br'
        usuario = User.objects.create_user(
            email=email,
            password=validated_data['password'],
            username=validated_data['username']
        )
        usuario.name = informacoes_usuario_json[0]['nm_pessoa']
        usuario.cpf = cpf
        usuario.is_active = False
        usuario.save()
        return usuario

    class Meta:
        model = User
        fields = ("username", "email", "name", "cpf")
