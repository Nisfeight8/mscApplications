from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class MscConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'msc'
    verbose_name = _("MSC Informations")
