from rest_framework import serializers

from ...models import Responsavel, Aluno


class ResponsavelSerializer(serializers.ModelSerializer):
    Aluno = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=Aluno.objects.all()
    )

    class Meta:
        model = Responsavel
        fields = '__all__'
