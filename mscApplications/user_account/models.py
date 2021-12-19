from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

from.validators import only_int
from.constants import GENDER_CHOICES

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_applicant = models.BooleanField(default=False)
    is_evaluator = models.BooleanField(default=False)

class Evaluator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='evaluator', on_delete=models.CASCADE,primary_key=True, verbose_name=_("User"))
    telephone = models.CharField(_('Telephone'),max_length = 10,validators=[only_int])
    committee = models.ForeignKey(Call,on_delete=models.SET_NULL,null=True, verbose_name=_("Committe"))

    def __str__(self):
        try:
            return self.user.first_name+" "+self.user.last_name
        except ObjectDoesNotExist:
            return self.telephone

class Applicant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='applicant',primary_key=True, verbose_name=_("User"))
    telephone = models.CharField(_('Telephone'),max_length = 10,validators=[only_int])
    address = models.CharField(_('Address'),max_length=50)
    city = models.CharField(_('City'),max_length=64)
    country = models.CharField(_('Country'),max_length=50)
    birth_date=models.DateField()
    gender = models.CharField(_('Gender'),max_length=1, choices=GENDER_CHOICES)
    citizenship = models.CharField(_('Citizenship'),max_length=64)

    def __str__(self):
        try:
            return self.user.first_name+" "+self.user.last_name
        except ObjectDoesNotExist:
            return self.telephone