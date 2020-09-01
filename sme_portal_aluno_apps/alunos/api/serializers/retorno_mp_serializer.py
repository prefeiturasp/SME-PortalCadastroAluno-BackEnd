import logging

from rest_framework import serializers

from ...models.retorno_mp import RetornoMP

log = logging.getLogger(__name__)


class RetornoMPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetornoMP
        fields = '__all__'


class RetornoMPCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetornoMP
        exclude = ('id', 'registro_processado')
