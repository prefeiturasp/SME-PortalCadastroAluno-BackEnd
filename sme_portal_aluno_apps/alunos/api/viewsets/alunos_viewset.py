from django.db.models import Q
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from ..serializers.aluno_serializer import (AlunoSerializer, AlunoLookUpSerializer, AlunoCreateSerializer)

from ...models.aluno import Aluno


class AlunosViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    lookup_field = 'codigo_eol'
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def get_queryset(self):
        queryset = self.queryset
        nome = self.request.query_params.get('nome')
        if nome is not None:
            queryset = queryset.filter(
                Q(nome__contains=nome) | Q(responsavel__nome__contains=nome))
        return queryset

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
