from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    cpf = CharField(_('CPF'), max_length=11, blank=True, null=True, unique=True,  # noqa DJ01
                    validators=[MinLengthValidator(11)])

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
