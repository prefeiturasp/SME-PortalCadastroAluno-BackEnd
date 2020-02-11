# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import viewsets
# from rest_framework.permissions import AllowAny
#
#
# from ..serializers.responsavel_serializer import (ResponsavelSerializer, ResponsavelLookUpSerializer,
#                                                   ResponsavelCreateSerializer)
# from ...models.aluno import Responsavel
#
#
# class ResponsaveisViewSet(viewsets.ModelViewSet):
#     permission_classes = [AllowAny]
#     lookup_field = 'uuid'
#     queryset = Responsavel.objects.all()
#     serializer_class = ResponsavelSerializer
#
#     def get_queryset(self):
#         return self.queryset
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return ResponsavelSerializer
#         elif self.action == 'list':
#             return ResponsavelLookUpSerializer
#         else:
#             return ResponsavelCreateSerializer
