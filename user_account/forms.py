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
    email = forms.EmailField(max_length=100, help_text='Required',required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, help_text=_('Existing email'),required=True,label=_("Email"))
    new_email = forms.EmailField(max_length=100, help_text=_('Enter new email'),required=True,label=_("New email"))
    confirm_email = forms.EmailField(max_length=100, help_text=_('Confirm email'),required=True,label=_("Confirm email"))
    class Meta:
        model = User
        fields = ('email','new_email','confirm_email')
    def clean(self):
        cleaned_data = super(EmailChangeForm, self).clean()
        new_email = self.cleaned_data.get('new_email')
        confirm_email=self.cleaned_data.get('confirm_email')
        print(new_email)
        print(confirm_email)
        if new_email != confirm_email:
            raise forms.ValidationError(
                _("New Email and Confirm Email does not match")
            )
        if new_email != self.instance.email:
            if User.objects.filter(email=new_email).exists():
                raise ValidationError(_("Email already exists"))
    def clean_email(self):
        email = self.cleaned_data['email']
        if email != self.instance.email:
            raise ValidationError(_("Email is wrong"))
        return email

class ApplicantForm(forms.ModelForm):
    MALE='M'
    FEMALE='F'
    GENDER_CHOICES = [
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    ]
    first_name = forms.CharField(label=_("First Name"),max_length=150)
    last_name = forms.CharField(label=_("Last Name"),max_length=150)
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,label=_("Birth Date"),help_text="(dd/mm/yyyy)")
    telephone = forms.CharField(label=_("Telephone"))
    address = forms.CharField(label=_("Address"))
    country = forms.CharField(label=_("Country"))
    city = forms.CharField(label=_("City"))
    citizenship = forms.CharField(label=_("Citizenship"))
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    class Meta:
        model = Applicant
        fields = ('first_name','last_name','telephone', 'address', 'city', 'country','birth_date','gender','citizenship')
    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.fields['gender'].label=_("Gender")
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
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

