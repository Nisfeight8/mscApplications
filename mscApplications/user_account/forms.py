from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from .models import User
from applicant.models import Applicant
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Field
from django.conf import settings
from applicant.constants import GENDER_CHOICES
from applicant.validators import only_int
from applicant.models import Applicant

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))
    birth_date = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        label=_("Birth Date"),
        help_text="(dd/mm/yyyy)",
        required=True
        
    )
    telephone = forms.CharField(label=_("Telephone"),max_length = 10,required=True, validators=[only_int])
    address = forms.CharField(label=_("Address"),required=True)
    country = forms.CharField(label=_("Country"),required=True)
    city = forms.CharField(label=_("City"),required=True)
    citizenship = forms.CharField(label=_("Citizenship"),required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES,label=_("Gender"),required=True)
    
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        Applicant.objects.create(
            user=user,
            telephone=self.cleaned_data['telephone'],
            citizenship=self.cleaned_data['citizenship'],
            gender=self.cleaned_data['gender'],
            city=self.cleaned_data['city'],
            country=self.cleaned_data['country'],
            address=self.cleaned_data['address'],
            birth_date=self.cleaned_data['birth_date'],
        )
        