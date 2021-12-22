from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from applicant.models import Applicant
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Field
from django.conf import settings


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First Name'),widget=forms.TextInput(attrs={'placeholder': _('First Name')}))
    last_name = forms.CharField(max_length=30, label=_('Last Name'),widget=forms.TextInput(attrs={'placeholder': _('Last Name')}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.fields["gender"].label = _("Gender")
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "telephone",
            Row(
                Column("birth_date", css_class="form-group col-md-6 mb-0"),
                Column("gender", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("country", css_class="form-group col-md-4 mb-0"),
                Column("city", css_class="form-group col-md-4 mb-0"),
                Column("address", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "citizenship",
        )
