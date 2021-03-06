from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class InstitutionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'institution'
    verbose_name = _("Institution Informations")
