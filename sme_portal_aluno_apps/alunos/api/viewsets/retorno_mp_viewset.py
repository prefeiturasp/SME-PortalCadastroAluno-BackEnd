from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from ...models import RetornoMP
from ..serializers.retorno_mp_serializer import (RetornoMPSerializer, RetornoMPCreateSerializer)


class RetornoMPViewset(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'uuid'
    queryset = RetornoMP.objects.all()
    serializer_class = RetornoMPSerializer

    def create(self, request, *args, **kwargs):
        for retorno in request.data.get('retornos'):
            novo_retorno = RetornoMP(
                codigo_eol=retorno.get('codigo_eol'),
                cpf=retorno.get('cpf'),
                status=retorno.get('status'),
                mensagem=retorno.get('mensagem'),
                data_ocorrencia=retorno.get('data_ocorrencia'),
            )
            novo_retorno.save()

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return RetornoMPCreateSerializer
    #     return RetornoMPSerializer
