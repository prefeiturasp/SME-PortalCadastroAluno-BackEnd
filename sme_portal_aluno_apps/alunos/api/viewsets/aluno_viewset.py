from django_filters import rest_framework as filters

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter


from ..serializers.aluno_serializer import AlunoSerializer, AlunoCreateSerializer
from ...models import Aluno


class AlunosViewSet(viewsets.ModelViewSet):

    permission_classes = [AllowAny]
    lookup_field = 'uuid'
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('end_uf', )
    ordering_fields = ('razao_social',)
    search_fields = ('uuid', 'cnpj')

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AlunoSerializer
        elif self.action == 'list':
            return AlunoSerializer
        else:
            return AlunoCreateSerializer

    # @action(detail=False)
    # def lookup(self, _):
        # return Response(AlunoLookUpSerializer(self.queryset.order_by('razao_social'), many=True).data)

