from django.db import models
from institution.models import Department
from utils.validators import telephone_validator
from django.utils.translation import gettext as _

from django.conf import settings


# Create your models here.
class Secretary(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='secretary', on_delete=models.CASCADE,primary_key=True)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    telephone = models.CharField(_('Telephone'),max_length = 10,validators=[telephone_validator])

    class Meta:
        verbose_name = _("Secretary")
        verbose_name_plural = _("Secretaries")