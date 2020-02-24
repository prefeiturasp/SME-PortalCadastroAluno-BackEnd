from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..serializers.aluno_serializer import (AlunoSerializer, AlunoLookUpSerializer, AlunoCreateSerializer)

from ...models.aluno import Aluno


class AlunosViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'codigo_eol'
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        nome_estudante = self.request.query_params.get('nome_estudante', None)
        nome_responsavel = self.request.query_params.get('nome_responsavel', None)

        if user.codigo_escola:
            queryset = queryset.filter(codigo_escola=user.codigo_escola)

        if nome_estudante:
            queryset = queryset.filter(nome__contains=nome_estudante)

        if nome_responsavel:
            queryset = queryset.filter(responsavel__nome__contains=nome_responsavel)

        return queryset.order_by('nome')

    def get_serializer_class(self):
        if self.action == 'list':
            return AlunoLookUpSerializer
        else:
            return AlunoCreateSerializer

    def retrieve(self, request, codigo_eol=None, **kwargs):
        aluno = Aluno.objects.get(codigo_eol=codigo_eol)
        data = AlunoSerializer(aluno).data
        responsaveis = [data['responsaveis']]
        data['responsaveis'] = responsaveis
        return Response(data)
