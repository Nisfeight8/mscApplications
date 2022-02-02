from django import forms
from user_account.models import User
from .models import Evaluator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.forms import UserCreationForm
from utils.validators import telephone_validator

class EvaluatorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))
    class Meta:
        model = Evaluator
        fields = ("first_name", "last_name", "telephone")

    def __init__(self, *args, **kwargs):
        super(EvaluatorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="form-group col-md-6 mb-0"),
                Column("last_name", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            "telephone",
        )

class EvaluatorCreateForm(UserCreationForm):
    telephone = forms.CharField(max_length=10, label=_('Telephone'),validators=[telephone_validator])

    class Meta:
        model = User
        fields = ('email','first_name','last_name','password1','password2','telephone')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(EvaluatorCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_evaluator=True
        if commit:
            user.save()
            Evaluator.objects.create(user=user,telephone=self.cleaned_data["telephone"],department=self.user.secretary.department)
        return user

class EvaluatorUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))

    class Meta:
        model = Evaluator
        fields = ('first_name','last_name','telephone')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(EvaluatorUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'

    def save(self, commit=True):
        evaluator = super().save(commit=False)
        if commit:
            evaluator.department=self.user.secretary.department
            evaluator.save()
            evaluator.user.first_name=self.cleaned_data['first_name']
            evaluator.user.last_name=self.cleaned_data['last_name']
            evaluator.user.save()
        return evaluator