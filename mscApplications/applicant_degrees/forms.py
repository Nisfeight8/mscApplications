from django import forms
from django.contrib.auth.models import User
from .models import *
from msc.models import MscFlow
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Div,Field
from django.conf import settings
from django.utils.translation import get_language
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class AdmittedFlowModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if get_language() =='en-us':
            return obj.title_en_us
        else:
            return obj.title_el_GR

class ApplicationAdmitForm(forms.ModelForm):
    admitted_flow=AdmittedFlowModelChoiceField(queryset=MscFlow.objects.none())
    class Meta:
        model = Application
        fields = ('admitted','admitted_flow')
class ApplicantForm(forms.ModelForm):
    MALE='M'
    FEMALE='F'
    GENDER_CHOICES = [
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    ]
    username = forms.CharField(max_length=150 ,validators=[UnicodeUsernameValidator()],help_text=_('This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'))
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
        fields = ('username','first_name','last_name','telephone', 'address', 'city', 'country','birth_date','gender','citizenship')
    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.fields['gender'].label=_("Gender")
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'username',
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

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.instance.user.username:
            if User.objects.filter(username=username).exists():
                raise ValidationError("Username already exists")
        return username

class DiplomaForm(forms.ModelForm):
    UNDERGRADUATE='UG'
    POSTGRADUATE='PG'
    TYPE_CHOICES = [
        (UNDERGRADUATE, _('Undergraduate')),
        (POSTGRADUATE, _('Postgraduate')),
    ]
    TYPE_CHOICES.insert(0, ('', ''))
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    date_awarded = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,label=_("Date Awarded"),help_text="(dd/mm/yyyy)")
    media_file = forms.FileField(help_text=_("supported type is pdf"),label=_("Media File"))
    class Meta:
        model = Diploma
        exclude = ('applicant',)
    def __init__(self, *args, **kwargs):
        super(DiplomaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
class ReferenceForm(forms.ModelForm):
    reference_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,label=_("Reference Date"),help_text="(dd/mm/yyyy)")
    media_file = forms.FileField(help_text=_("supported type is pdf"),label=_("Media File"))
    class Meta:
        model = Reference
        exclude = ('applicant',)
    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
# helper class: returning full_name instead of username
class PreferenceModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        if get_language() =='en-us':
            return obj.title_en_us
        else:
            return obj.title_el_GR

class ApplicationForm(forms.ModelForm):
    preferences=PreferenceModelChoiceField(queryset=MscFlow.objects.none())
    class Meta:
        model = Application
        fields = ('preferences','reference','comments')
    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.fields['reference'].label=_("Reference")
        self.fields['comments'].label=_("Comments")
class PhdForm(forms.ModelForm):
    UNDERGRADUATE='UG'
    POSTGRADUATE='PG'
    TYPE_CHOICES = [
        (UNDERGRADUATE, _('Undergraduate')),
        (POSTGRADUATE, _('Postgraduate')),
    ]
    TYPE_CHOICES.insert(0, ('', ''))
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    date_awarded = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,label=_("Date Awarded"),help_text="(dd/mm/yyyy)")
    media_file = forms.FileField(help_text=_("supported type is pdf"),label=_("Media File"))
    class Meta:
        model = Phd
        exclude = ('applicant',)
    def __init__(self, *args, **kwargs):
        super(PhdForm, self).__init__(*args, **kwargs)
        self.fields['type'].initial = None
        self.helper = FormHelper()
        self.helper.form_show_labels = False
class JobExperienceForm(forms.ModelForm):
    start_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,label=_("Start Date"),help_text="(dd/mm/yyyy)")
    end_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,label=_("End Date"),help_text="(dd/mm/yyyy)")
    media_file = forms.FileField(help_text=_("supported type is pdf"),label=_("Media File"))
    class Meta:
        model = JobExperience
        exclude = ('applicant',)
    def __init__(self, *args, **kwargs):
        super(JobExperienceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False