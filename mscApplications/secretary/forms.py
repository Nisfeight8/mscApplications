from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django.utils.translation import gettext_lazy as _
from .models import Secretary

class SecretaryForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))
    class Meta:
        model = Secretary
        fields = ("first_name", "last_name", "telephone")

    def __init__(self, *args, **kwargs):
        super(SecretaryForm, self).__init__(*args, **kwargs)
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
