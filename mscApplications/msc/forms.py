from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper

class ApplicationAdmitForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ("admitted", "admitted_flow")

class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ("preferences", "reference", "comments")

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields["reference"].label = _("Reference")
        self.fields["comments"].label = _("Comments")
        self.helper = FormHelper()  
        self.helper.form_tag = False

class CallForm(forms.ModelForm):

    class Meta:
        model = Call
        fields = ("title_en", "title_el","start_date","end_date", "msc_programme","evaluators")

    def __init__(self, *args, **kwargs):
        super(CallForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget=forms.TextInput(attrs={'type': 'date'})
        self.fields['end_date'].widget=forms.TextInput(attrs={'type': 'date'})
        self.fields['title_en'].required=True
        self.fields['title_el'].required=True
        self.helper = FormHelper()  
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'

    def clean(self):
        if self.cleaned_data.get("start_date")>self.cleaned_data.get("end_date"):
            raise forms.ValidationError({'end_date': ['End date should be greater than start date.', ]})

class MscFlowForm(forms.ModelForm):

    class Meta:
        model = MscFlow
        fields = ("title_en", "title_el")

    def __init__(self, *args, **kwargs):
        super(MscFlowForm, self).__init__(*args, **kwargs)
        self.fields['title_en'].required=True
        self.fields['title_el'].required=True
        self.helper = FormHelper()  
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'

class MscProgrammeForm(forms.ModelForm):

    class Meta:
        model = MscProgramme
        fields=('title_en','title_el','country_en','country_el','city_en','city_el','address_en','address_el','pobox','telephone')

    def __init__(self, *args, **kwargs):
        super(MscProgrammeForm, self).__init__(*args, **kwargs)
        self.fields['title_en'].required=True
        self.fields['title_el'].required=True
        self.fields['country_en'].required=True
        self.fields['country_el'].required=True
        self.fields['city_en'].required=True
        self.fields['city_el'].required=True
        self.fields['address_en'].required=True
        self.fields['address_el'].required=True
        self.helper = FormHelper()  
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        