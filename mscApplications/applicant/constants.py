from django.utils.translation import gettext as _


MALE='M'
FEMALE='F'
GENDER_CHOICES = [
    (MALE, _('Male')),
    (FEMALE, _('Female')),
]

UNDERGRADUATE='UG'
POSTGRADUATE='PG'
TYPE_CHOICES = [
    (UNDERGRADUATE, _('Undergraduate')),
    (POSTGRADUATE, _('Postgraduate')),
]