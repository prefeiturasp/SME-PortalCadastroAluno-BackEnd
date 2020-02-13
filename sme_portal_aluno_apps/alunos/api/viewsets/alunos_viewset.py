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
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return AlunoLookUpSerializer
        else:
            return AlunoCreateSerializer

    def retrieve(self, request, codigo_eol=None):
        aluno = Aluno.objects.get(codigo_eol=codigo_eol)
        data = AlunoSerializer(aluno).data
        responsaveis = [data['responsaveis']]
        data['responsaveis'] = responsaveis
        return Response(data)
