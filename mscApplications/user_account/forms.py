from django import forms
from applicant.models import Applicant
from django.utils.translation import gettext_lazy as _
from applicant.models import Applicant

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First Name'), widget=forms.TextInput(attrs={'placeholder': _('First Name')}))
    last_name = forms.CharField(max_length=30, label=_('Last Name'), widget=forms.TextInput(attrs={'placeholder': _('Last Name')}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_applicant=True
        user.save()
