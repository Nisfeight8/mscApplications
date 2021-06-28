from django.shortcuts import render
from msc.models import MscFlow,Evaluator,Call
from msc.forms import EvaluatorForm
from applicant_degrees.models import *
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView,DetailView,TemplateView
from extra_views import UpdateWithInlinesView, InlineFormSetFactory
from applicant_degrees.forms import ApplicationAdmitForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


class EvaluatorHomeView(TemplateView):
    template_name='evaluator_home.html'

class CallDetailView(PermissionRequiredMixin,DetailView):
    model = Call
    template_name = 'call_applications.html'
    context_object_name = 'call'
    permission_required = ('msc.view_call',)
    def get_context_data(self, **kwargs):
        context = super(CallDetailView, self).get_context_data(**kwargs)
        context['msc_flows'] =MscFlow.objects.filter(msc_programme=self.object.msc_programme)
        context['applications'] =Application.objects.filter(call=self.object).order_by('-submission_date')
        return context
    def get_object(self,queryset=None):
        return self.request.user.evaluator.committee



class ApplicationAdmitView(PermissionRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Application
    form_class=ApplicationAdmitForm
    template_name = 'application_admit.html'
    permission_required = ('applicant_degrees.change_application',)
    success_message = _('Application admitted !')
    success_url =reverse_lazy('evaluator:call_applications')
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['admitted'].label = ""
        form.fields['admitted_flow'].queryset = self.object.preferences.all()
        form.fields['admitted_flow'].label = ""
        return form

class ApplicantDetailView(PermissionRequiredMixin,DetailView):
    model = Applicant
    template_name = 'applicant_detail.html'
    context_object_name = 'applicant'
    permission_required = ('applicant_degrees.view_applicant',)

class ProfileDetailView(PermissionRequiredMixin,DetailView):
    model=Evaluator
    context_object_name = 'evaluator'
    template_name = 'evaluator_profile.html'
    permission_required = ('msc.change_evaluator',)
    def get_object(self,queryset=None):
        return self.request.user.evaluator

class ProfileUpdateView(PermissionRequiredMixin,UpdateView):
    model = Evaluator
    form_class=EvaluatorForm
    template_name = 'evaluator_profile_edit.html'
    permission_required = ('msc.change_evaluator',)
    success_url = reverse_lazy('evaluator:evaluator_profile')
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['first_name'].initial = self.request.user.first_name
        form.fields['last_name'].initial = self.request.user.last_name
        form.fields['username'].initial = self.request.user.username
        return form
    def form_valid(self,form):
        evaluator = form.save(commit=False)
        evaluator.user.first_name=form.cleaned_data['first_name']
        evaluator.user.last_name=form.cleaned_data['last_name']
        evaluator.user.username=form.cleaned_data['username']
        evaluator.user.save()
        evaluator.save()
        messages.success(self.request, (_('Your profile has been updated.')))
        return super().form_valid(form)
    def get_object(self,queryset=None):
        return self.request.user.evaluator
