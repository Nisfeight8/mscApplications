from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class EvaluatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'evaluator'
    verbose_name = _("Evaluator")
