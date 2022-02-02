from django.views.generic import DetailView,ListView, UpdateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from msc.models import Call, MscProgramme
from evaluator.models import Evaluator
from .models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import *
from utils.mixins import SecretaryRequiredMixin
# Create your views here.

class SecretaryHome(LoginRequiredMixin,SecretaryRequiredMixin,TemplateView):
    template_name = 'secretary_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department']=self.request.user.secretary.department
        return context


class SecretaryProfileDetailView(LoginRequiredMixin,SecretaryRequiredMixin,DetailView):
    model=Secretary
    context_object_name = 'secretary'
    template_name = 'secretary_profile.html'

    def get_object(self):
        return self.request.user.secretary


class SecretaryProfileUpdateView(LoginRequiredMixin,SuccessMessageMixin,SecretaryRequiredMixin,UpdateView):
    model = Secretary
    form_class=SecretaryForm
    template_name = 'secretary_profile_edit.html'
    success_url = reverse_lazy('secretary:secretary_profile')
    success_message = _('Your profile has been updated.')

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
        return super().form_valid(form)

    def get_object(self):
        return self.request.user.secretary

class SecretaryMscProgrammeListView(LoginRequiredMixin,SecretaryRequiredMixin,ListView):
    models =MscProgramme
    template_name = 'secretary_msc_programme_list.html'
    context_object_name='programmes'

    def get_queryset(self):
        return MscProgramme.objects.filter(department=self.request.user.secretary.department)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department']=self.request.user.secretary.department
        return context

class SecretaryEvaluatorListView(LoginRequiredMixin,SecretaryRequiredMixin,ListView):
    models =Evaluator
    template_name = 'secretary_evaluator_list.html'
    context_object_name='evaluators'

    def get_queryset(self):
        return Evaluator.objects.filter(department=self.request.user.secretary.department)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department']=self.request.user.secretary.department
        return context


class SecretaryCallListView(LoginRequiredMixin,SecretaryRequiredMixin,ListView):
    models =Call
    template_name = 'secretary_call_list.html'
    context_object_name='calls'

    def get_queryset(self):
        return Call.objects.filter(msc_programme__department=self.request.user.secretary.department)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['department']=self.request.user.secretary.department
        return context