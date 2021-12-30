from msc.models import Call
from .forms import EvaluatorForm
from .models import Evaluator
from django.views.generic import UpdateView,DetailView,TemplateView,ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from utils.mixins import *
from django.contrib.auth.mixins import LoginRequiredMixin


class EvaluatorHomeView(LoginRequiredMixin,EvaluatorRequiredMixin,TemplateView):
    template_name='evaluator_home.html'


class EvaluatorProfileDetailView(LoginRequiredMixin,EvaluatorRequiredMixin,DetailView):
    model=Evaluator
    context_object_name = 'evaluator'
    template_name = 'evaluator_profile.html'

    def get_object(self,queryset=None):
        return self.request.user.evaluator


class EvaluatorProfileUpdateView(LoginRequiredMixin,EvaluatorRequiredMixin,UpdateView):
    model = Evaluator
    form_class=EvaluatorForm
    template_name = 'evaluator_profile_edit.html'
    success_url = reverse_lazy('evaluator:evaluator_profile')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['first_name'].initial = self.request.user.first_name
        form.fields['last_name'].initial = self.request.user.last_name
        return form

    def form_valid(self,form):
        user=form.instance.user
        user.first_name=form.cleaned_data['first_name']
        user.last_name=form.cleaned_data['last_name']
        user.save()
        messages.success(self.request, (_('Your profile has been updated.')))
        return super().form_valid(form)

    def get_object(self,queryset=None):
        return self.request.user.evaluator


class EvaluatorCallListView(LoginRequiredMixin,EvaluatorRequiredMixin,ListView):
    model=Call
    context_object_name='calls'
    template_name='evaluator_calls.html'

    def get_queryset(self):
        queryset = Call.objects.filter(evaluators__pk=self.request.user.id)
        return queryset