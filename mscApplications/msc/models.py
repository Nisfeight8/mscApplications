from django.db import models
from institution.models import Department
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError



def only_int(value):
    if value.isdigit()==False:
        raise ValidationError(_('Only digits allowed'))
    elif len(value)<10:
        raise ValidationError(_('Telephone must have 10 digits'))

class MscProgramme(models.Model):
    title = models.CharField(_('Title'),max_length = 200)
    address = models.CharField(_('Address'),max_length=50)
    pobox = models.CharField(_('Pobox'),max_length=5)
    city = models.CharField(_('City'),max_length=65)
    country = models.CharField(_('Country'),max_length=50)
    telephone = models.CharField(_('Telephone'),max_length = 10,validators=[only_int])
    department=models.ForeignKey(Department,on_delete=models.CASCADE, verbose_name=_("Department"))
    def __str__(self):
        return self.title
class MscFlow(models.Model):
    title = models.CharField(_('Title'),max_length = 200)
    msc_programme=models.ForeignKey(MscProgramme,on_delete=models.CASCADE,verbose_name=_("Msc Programme"))
    def __str__(self):
        return self.title
class Call(models.Model):
    title = models.CharField(_('Title'),max_length = 200)
    start_date=models.DateField(_('Start date'))
    end_date=models.DateField(_('End Date'))
    msc_programme=models.ForeignKey(MscProgramme,on_delete=models.CASCADE, verbose_name=_("Msc Programme"))
    def __str__(self):
        return self.title
class Evaluator(models.Model):
    user = models.OneToOneField(User,related_name='evaluator', on_delete=models.CASCADE,primary_key=True, verbose_name=_("User"))
    telephone = models.CharField(_('Telephone'),max_length = 10,validators=[only_int])
    committee = models.ForeignKey(Call,on_delete=models.SET_NULL,null=True, verbose_name=_("Committe"))
    def __str__(self):
        try:
            return self.user.first_name+" "+self.user.last_name
        except ObjectDoesNotExist:
            return self.telephone