from msc.models import MscFlow
from django import forms
from .models import Application
from django.utils.translation import gettext_lazy as _

class ApplicationAdmitForm(forms.ModelForm):
    admitted_flow = forms.ModelChoiceField(queryset=MscFlow.objects.none())

    class Meta:
        model = Application
        fields = ("admitted", "admitted_flow")

class ApplicationForm(forms.ModelForm):
    preferences = forms.ModelMultipleChoiceField(queryset=MscFlow.objects.none())

    class Meta:
        model = Application
        fields = ("preferences", "reference", "comments")

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields["reference"].label = _("Reference")
        self.fields["comments"].label = _("Comments")
