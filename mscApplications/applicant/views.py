from .models import *
from msc.models import *

from .forms import *
from utils import pdf_generator
from utils.mixins import ApplicantCompleteProfileMixin
import uuid
from .models import *

from extra_views import  UpdateWithInlinesView, InlineFormSetFactory

from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView, CreateView,TemplateView, UpdateView
from django.shortcuts import get_object_or_404,redirect
from django.http import FileResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

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


class ApplicationCreateView(LoginRequiredMixin,ApplicantRequiredMixin,ApplicantCompleteProfileMixin,CreateView):
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
            form.fields['preferences'].required = True
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
        if self.request.LANGUAGE_CODE =='en':
            file_data= pdf_generator.generate_applicant_app(self.request.user.applicant,application)
        else:
            file_data= pdf_generator.generate_applicant_app_to_greek(self.request.user.applicant,application)
        application.media_file.save(self.request.user.email+uuid.uuid4().hex[:6].upper()+".pdf", file_data, save=False)
        application.save()
        return FileResponse(application.media_file)


class ApplicationAdmitView(LoginRequiredMixin,EvaluatorRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Application
    form_class=ApplicationAdmitForm
    template_name = 'application_admit.html'
    success_message = _('Application admitted !')
    success_url =reverse_lazy('msc:call_application_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['admitted'].label = ""
        form.fields['admitted_flow'].queryset = self.object.preferences.all()
        form.fields['admitted_flow'].label = ""
        return form

    def get_success_url(self):
        return reverse('msc:call_application_list',kwargs={'pk':self.kwargs['call_id']} )

class ApplicantDetailView(LoginRequiredMixin,EvaluatorRequiredMixin,DetailView):
    model = Applicant
    template_name = 'applicant_detail.html'
    context_object_name = 'applicant'

