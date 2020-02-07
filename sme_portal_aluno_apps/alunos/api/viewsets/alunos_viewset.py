from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from ..serializers.aluno_serializer import AlunoSerializer, AlunoCreateSerializer, AlunoLookUpSerializer
from ...models.aluno import Aluno


class AlunosViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AlunoSerializer
        elif self.action == 'list':
            return AlunoLookUpSerializer
        else:
            return AlunoCreateSerializer

    @action(detail=False, url_path='titulos-modelo-ateste')
    def lookup(self, _):
        return Response(AlunoLookUpSerializer(self.queryset.order_by('-criado_em'), many=True).data)
