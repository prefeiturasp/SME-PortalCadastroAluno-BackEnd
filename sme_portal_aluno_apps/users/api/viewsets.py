from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer
from ...eol_servico.utils import EOLException

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    def create(self, request):  # noqa C901
        try:
            assert not User.objects.filter(
                username=request.data.get('username')
            ).exists(), 'Usuário existente no sistema'
            usuario = UserSerializer().create(request.data)
            usuario.enviar_email_confirmacao()
            return Response(UserSerializer(usuario).data)
        except ValidationError as e:
            return Response({'detail': e.detail[0].title()}, status=status.HTTP_400_BAD_REQUEST)
        except AssertionError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except EOLException as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UsuarioConfirmaEmailViewSet(GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def list(self, request, uuid, confirmation_key):  # noqa C901
        try:
            usuario = User.objects.get(uuid=uuid)
            usuario.confirm_email(confirmation_key)
            usuario.is_active = usuario.is_confirmed
            usuario.save()
        except ObjectDoesNotExist:
            return Response({'detail': 'Erro ao confirmar email'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializer(usuario).data)
