from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from ..core.helpers.enviar_email import enviar_email
from ..core.models_abstracts import TemChaveExterna
from ..core.utils import url_configs


class User(SimpleEmailConfirmationUserMixin, AbstractUser, TemChaveExterna):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    cpf = CharField(_('CPF'), max_length=11, blank=True, null=True, unique=True,  # noqa DJ01
                    validators=[MinLengthValidator(11)])
    codigo_escola = CharField("Código EOL da Escola", max_length=10, blank=True, null=True)
    nome_escola = CharField("Nome da Escola", max_length=100, blank=True, null=True)
    codigo_dre = CharField("Código EOL da DRE", max_length=10, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def enviar_email_confirmacao(self):
        self.add_email_if_not_exists(self.email)
        content = {'uuid': self.uuid, 'confirmation_key': self.confirmation_key}
        conteudo = (f'Clique neste link para confirmar seu e-mail no Pedido de Uniformes: ' +
                    f'{url_configs("CONFIRMAR_EMAIL", content)}')
        enviar_email(
            assunto='Confirme seu e-mail - Pedido de Uniformes',
            mensagem=conteudo,
            enviar_para=self.email
        )
