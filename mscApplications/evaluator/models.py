from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _

from utils.validators import telephone_validator
from institution.models import Department
from django.conf import settings

class Evaluator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='evaluator', on_delete=models.CASCADE,primary_key=True)
    telephone = models.CharField(_('Telephone'),max_length = 10,validators=[telephone_validator])
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        try:
            return self.user.first_name+" "+self.user.last_name
        except ObjectDoesNotExist:
            return self.telephone

    class Meta:
        verbose_name = _("Evaluator")
        verbose_name_plural = _("Evaluators")