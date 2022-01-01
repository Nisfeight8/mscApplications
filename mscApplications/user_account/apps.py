from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UserAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_account'
    verbose_name = _("User Account")

    def ready(self):
        import user_account.signals
