from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

def only_int(value):
    if value.isdigit()==False:
        raise ValidationError(_('Only digits allowed'))
    elif len(value)<10:
        raise ValidationError(_('Telephone must have 10 digits'))

class Institution(models.Model):
    title = models.CharField(_('Title'),max_length = 200)
    address = models.CharField(_('Address'),max_length=50)
    pobox = models.CharField(_('Pobox'),max_length=5)
    city = models.CharField(_('City'),max_length=64)
    country = models.CharField(_('Country'),max_length=50)
    telephone = models.CharField(_('Telephone'),max_length = 10,validators=[only_int])
    def __str__(self):
        return self.title
class Department(models.Model):
    title = models.CharField(_('Title'),max_length = 200)
    address = models.CharField(_('Address'),max_length=50)
    pobox = models.CharField(_('Pobox'),max_length=5)
    city = models.CharField(_('City'),max_length=64)
    country = models.CharField(_('Country'),max_length=50)
    telephone = models.CharField(_('Telephone'),max_length = 10,validators=[only_int])
    institution=models.ForeignKey(Institution,on_delete=models.CASCADE,verbose_name=_('Institution'))
    def __str__(self):
        return self.title