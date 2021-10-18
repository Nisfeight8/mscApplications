from django import forms
from django.contrib.auth.models import User
from .models import Evaluator
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Div,Field
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class EvaluatorForm(forms.ModelForm):
    username = forms.CharField(max_length=150 ,validators=[UnicodeUsernameValidator()],help_text=_('This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'))
    first_name = forms.CharField(label=_("First Name"),max_length=150)
    last_name = forms.CharField(label=_("Last Name"),max_length=150)
    telephone = forms.CharField(label=_("Telephone"))
    class Meta:
        model = Evaluator
        fields = ('username','first_name','last_name','telephone')
    def __init__(self, *args, **kwargs):
        super(EvaluatorForm, self).__init__(*args, **kwargs)
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
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.instance.user.username:
            if User.objects.filter(username=username).exists():
                raise ValidationError("Username already exists")
        return username