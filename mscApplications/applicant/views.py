from .models import *

from .forms import *
from .models import *

from msc.models import Application

from extra_views import  UpdateWithInlinesView, InlineFormSetFactory

from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView,DetailView,TemplateView
from django.utils.translation import ugettext_lazy as _

from utils.mixins import *
from django.contrib.auth.mixins import LoginRequiredMixin

class ApplicantHomeView(LoginRequiredMixin,ApplicantRequiredMixin,TemplateView):
    template_name = 'applicant_home.html'


class ApplicantProfileDetailView(LoginRequiredMixin,ApplicantRequiredMixin,DetailView):
    model=Applicant
    context_object_name = 'applicant'
    template_name = 'applicant_profile.html'

    def get_object(self,queryset=None):
        return self.request.user.applicant


class DiplomaInline(InlineFormSetFactory):
    model = Diploma
    form_class=DiplomaForm
    factory_kwargs = {'extra': 1}

class PhdInline(InlineFormSetFactory):
    model = Phd
    form_class=PhdForm
    factory_kwargs = {'extra': 1}


class JobExperienceInline(InlineFormSetFactory):
    model = JobExperience
    form_class=JobExperienceForm
    factory_kwargs = {'extra': 1}


class ReferenceInline(InlineFormSetFactory):
    model = Reference
    form_class=ReferenceForm
    factory_kwargs = {'extra': 1}


class ApplicantProfileUpdateView(LoginRequiredMixin,ApplicantRequiredMixin,UpdateWithInlinesView):
    model = Applicant
    inlines = [ DiplomaInline,PhdInline, JobExperienceInline,ReferenceInline]
    form_class=ApplicantForm
    template_name = 'applicant_profile_edit.html'

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

    def get_object(self,queryset=None):
        return self.request.user.applicant

    def get_success_url(self):
        messages.success(self.request, (_('Your profile has been updated.')))
        if 'next' in self.request.GET:
            return self.request.GET['next']
        return reverse('applicant:applicant_profile')


class ApplicantDetailView(LoginRequiredMixin,EvaluatorOrSecretaryRequiredMixin,DetailView):
    model = Applicant
    template_name = 'applicant_detail.html'
    context_object_name = 'applicant'

class ApplicantApplicationListView(LoginRequiredMixin,ApplicantRequiredMixin,ListView):
    model = Application
    template_name = 'applicant_application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        queryset = Application.objects.filter(applicant=self.request.user.applicant)
        return queryset