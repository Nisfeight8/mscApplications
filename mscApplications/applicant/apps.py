from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ApplicantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applicant'
    verbose_name = _("Applicant")
