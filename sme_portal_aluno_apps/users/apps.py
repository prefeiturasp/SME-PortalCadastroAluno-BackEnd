from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "sme_portal_aluno_apps.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import sme_portal_aluno_apps.users.signals  # noqa F401
        except ImportError:
            pass
