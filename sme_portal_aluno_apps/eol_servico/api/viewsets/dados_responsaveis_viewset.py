from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ...utils import EOLException, EOLService


class DadosResponsavelEOLViewSet(ViewSet):
    lookup_field = 'codigo_eol'
    permission_classes = (IsAuthenticated,)
    many = False

    @action(detail=False, methods=['post'])
    def busca_dados(self, request):
        try:
            dados = EOLService.get_informacoes_responsavel(request.data["codigo_eol"])
            return Response({'detail': dados})
        except EOLException as e:
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
