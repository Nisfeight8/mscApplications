from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from applicant_degrees.models import Applicant
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Div,Field
from django.conf import settings

class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1', 'password2')

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude=('user',)

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.fields['gender'].label=_("Gender")
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'telephone',
            Row(
                Column('birth_date', css_class='form-group col-md-6 mb-0'),
                Column('gender', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('country', css_class='form-group col-md-4 mb-0'),
                Column('city', css_class='form-group col-md-4 mb-0'),
                Column('address', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'citizenship',
        )

