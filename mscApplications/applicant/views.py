from .models import *
from user_account.models import Applicant
from msc.models import *

from .forms import *
from utils import pdf_generator

import datetime

import uuid

from django.views.generic import ( ListView, CreateView, DetailView,TemplateView)
from django.contrib import messages
from django.shortcuts import get_object_or_404,render
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import FileResponse
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import activate

class ApplicantHomeView(TemplateView):
    template_name = 'applicant_home.html'

class ProfileDetailView(DetailView):
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


class ProfileUpdateView(UpdateWithInlinesView):
    model = Applicant
    inlines = [ DiplomaInline,PhdInline, JobExperienceInline,ReferenceInline]
    form_class=ApplicantForm
    template_name = 'applicant_profile_edit.html'
    success_url = reverse_lazy('applicant:applicant_profile')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['first_name'].initial = self.request.user.first_name
        form.fields['last_name'].initial = self.request.user.last_name
        form.fields['username'].initial = self.request.user.username
        return form

    def form_valid(self,form):
        applicant = form.save(commit=False)
        applicant.user.first_name=form.cleaned_data['first_name']
        applicant.user.last_name=form.cleaned_data['last_name']
        applicant.user.username=form.cleaned_data['username']
        applicant.user.save()
        applicant.save()
        messages.success(self.request, (_('Your profile has been updated.')))
        return super().form_valid(form)

    def get_object(self,queryset=None):
        return self.request.user.applicant

class ApplicationCreateView(CreateView):
    model=Application
    template_name='application_create.html'
    form_class=ApplicationForm

    def get_context_data(self, **kwargs):
        context = super(ApplicationCreateView, self).get_context_data(**kwargs)
        context['call'] =Call.objects.get(id=self.kwargs['pk'])
        return context

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        call=Call.objects.get(id=self.kwargs['pk'])
        if call.msc_programme.mscflow_set.all:
            form.fields['preferences'].widget.attrs['required'] = 'required'
        form.fields['preferences'].queryset = MscFlow.objects.filter(msc_programme=call.msc_programme)
        form.fields['reference'].queryset = Reference.objects.filter(applicant=self.request.user.applicant)
        form.fields['preferences'].label = _("Select flows by the order you prefer")
        return form

    def form_valid(self, form):
        application = form.save(commit=False)
        application.applicant=self.request.user.applicant
        application.call= get_object_or_404(Call, id=self.kwargs['pk'])
        application.save()
        for index,flow_id in enumerate(self.request.POST.getlist('preferences')):
            application.preferences.add(int(flow_id), through_defaults={'priority': index+1})
        file_data=None
        if self.request.LANGUAGE_CODE =='en-us':
            file_data= pdf_generator.generate_applicant_app(self.request.user.applicant,application)
        else:
            file_data= pdf_generator.generate_applicant_app_to_greek(self.request.user.applicant,application)
        application.media_file.save(self.request.user.username+uuid.uuid4().hex[:6].upper()+".pdf", file_data, save=False)
        application.save()
        return FileResponse(application.media_file)

class CallListView(ListView):
    model = Call
    template_name = 'call_list.html'
    context_object_name = 'calls'

    def get_queryset(self) :
        queryset = Call.objects.filter(Q(end_date__gte=datetime.datetime.now())&Q(start_date__lte=datetime.datetime.now()))
        return queryset

class CallDetailView(DetailView):
    model = Call
    template_name = 'call_detail.html'
    context_object_name = 'call'

    def get_context_data(self, **kwargs):
        context = super(CallDetailView, self).get_context_data(**kwargs)
        context['msc_flows'] =MscFlow.objects.filter(msc_programme=self.object.msc_programme)
        context['evaluators'] =Evaluator.objects.filter(committee=self.object)
        return context