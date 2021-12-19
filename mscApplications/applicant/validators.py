from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def only_int(value):
    if value.isdigit()==False:
        raise ValidationError(_('Only digits allowed'))
    elif len(value)<10:
        raise ValidationError(_('Telephone must have 10 digits'))