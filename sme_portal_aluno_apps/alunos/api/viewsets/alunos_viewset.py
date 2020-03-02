from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from ..serializers.aluno_serializer import (AlunoSerializer, AlunoLookUpSerializer, AlunoCreateSerializer,
                                            AlunoSerializerComCPFEol)
from ....eol_servico.utils import EOLService, EOLException
from ...models.aluno import Aluno


class AlunosViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo_eol'
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        codigo_eol = self.request.query_params.get('codigo_eol', None)
        nome_estudante = self.request.query_params.get('nome_estudante', None)
        nome_responsavel = self.request.query_params.get('nome_responsavel', None)

        if codigo_eol:
            queryset = queryset.filter(codigo_eol=codigo_eol)
            if not queryset and user.codigo_escola:
                EOLService.cria_aluno_desatualizado(codigo_eol=codigo_eol)

        if user.codigo_escola:
            queryset = queryset.filter(codigo_escola=user.codigo_escola)

        if nome_estudante:
            queryset = queryset.filter(nome=nome_estudante)

        if nome_responsavel:
            queryset = queryset.filter(responsavel__nome=nome_responsavel)

        return queryset.order_by('nome')

    def get_serializer_class(self):
        if self.action == 'list':
            return AlunoLookUpSerializer
        else:
            return AlunoCreateSerializer

    def list(self, request, *args, **kwargs):
        try:
            return Response(AlunoLookUpSerializer(self.get_queryset(), many=True).data)
        except EOLException as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, codigo_eol=None, **kwargs):
        try:
            aluno = Aluno.objects.get(codigo_eol=codigo_eol)
            data = AlunoSerializerComCPFEol(aluno).data
            responsaveis = [data['responsaveis']]
            data['responsaveis'] = responsaveis
            return Response(data)
        except Aluno.DoesNotExist:
            return Response({'detail': 'Aluno não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
