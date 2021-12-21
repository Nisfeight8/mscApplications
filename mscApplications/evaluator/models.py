from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _

from .validators import only_int
from msc.models import Call
from django.conf import settings

class Evaluator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='evaluator', on_delete=models.CASCADE,primary_key=True, verbose_name=_("User"))
    telephone = models.CharField(_('Telephone'),max_length = 10,validators=[only_int])
    committee = models.ForeignKey(Call,on_delete=models.SET_NULL,null=True, verbose_name=_("Committe"))

    def __str__(self):
        try:
            return self.user.first_name+" "+self.user.last_name
        except ObjectDoesNotExist:
            return self.telephone

