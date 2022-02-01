from django import forms
from .models import *
from .constants import GENDER_CHOICES, TYPE_CHOICES
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext_lazy as _



class ApplicantForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First Name"), max_length=30)
    last_name = forms.CharField(label=_("Last Name"), max_length=30)
    birth_date = forms.DateField(
        label=_("Birth Date"),
        required=True,
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    telephone = forms.CharField(label=_("Telephone"),required=True)
    address = forms.CharField(label=_("Address"),required=True)
    country = forms.CharField(label=_("Country"),required=True)
    city = forms.CharField(label=_("City"),required=True)
    citizenship = forms.CharField(label=_("Citizenship"),required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES,label=_("Gender"),required=True)

    class Meta:
        model = Applicant
        fields = (
            "first_name",
            "last_name",
            "telephone",
            "address",
            "city",
            "country",
            "birth_date",
            "gender",
            "citizenship",
        )

    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="form-group col-md-6 mb-0"),
                Column("last_name", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
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


class DiplomaForm(forms.ModelForm):
    TYPE_CHOICES.insert(0, ("", ""))
    type = forms.ChoiceField(choices=TYPE_CHOICES, initial=None)
    media_file = forms.FileField(
        help_text=_("supported type is pdf"), label=_("Media File")
    )
    date_awarded = forms.DateField(
        label=_("Date Awarded"),
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Diploma
        exclude = ("applicant",)

    def __init__(self, *args, **kwargs):
        super(DiplomaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class ReferenceForm(forms.ModelForm):
    reference_date = forms.DateField(
        label=_("Reference Date"),
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    media_file = forms.FileField(
        help_text=_("supported type is pdf"), label=_("Media File")
    )

    class Meta:
        model = Reference
        exclude = ("applicant",)

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class PhdForm(forms.ModelForm):
    #TYPE_CHOICES.insert(0, ("", ""))
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    date_awarded = forms.DateField(
        label=_("Date Awarded"),
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    media_file = forms.FileField(
        help_text=_("supported type is pdf"), label=_("Media File")
    )

    class Meta:
        model = Phd
        exclude = ("applicant",)

    def __init__(self, *args, **kwargs):
        super(PhdForm, self).__init__(*args, **kwargs)
        self.fields["type"].initial = None
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class JobExperienceForm(forms.ModelForm):
    start_date = forms.DateField(
        label=_("Start Date"),
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    end_date = forms.DateField(
        label=_("End Date"),
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    media_file = forms.FileField(
        help_text=_("supported type is pdf"), label=_("Media File")
    )

    class Meta:
        model = JobExperience
        exclude = ("applicant",)

    def __init__(self, *args, **kwargs):
        super(JobExperienceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
