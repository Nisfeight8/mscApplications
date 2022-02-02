from django.db.models import Q
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from extra_views import  CreateWithInlinesView,UpdateWithInlinesView, InlineFormSetFactory

from .models import *

from .filters import MscProgrammeFilter
from .forms import *

from utils.mixins import *
from utils import pdf_generator

import uuid
import datetime

# Applications
class ApplicationListView(LoginRequiredMixin,EvaluatorOrSecretaryRequiredMixin,UserPassesTestMixin,ListView):
    model=Application
    template_name= 'application/application_list.html'
    context_object_name='applications'

    def get_queryset(self):
        call = Call.objects.get(id=self.kwargs['pk'])
        applications= Application.objects.filter(call=call).order_by('-submission_date')
        return applications

    def test_func(self):
        call = Call.objects.get(id=self.kwargs['pk'])
        user = self.request.user
        if user.is_evaluator:
            evaluator=user.evaluator
            if evaluator in call.evaluators.all():
                return True
        if user.is_secretary:
            if call.msc_programme.department==user.secretary.department:
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ApplicationListView, self).get_context_data(**kwargs)
        context['call']=Call.objects.get(id=self.kwargs['pk'])
        return context


class ApplicationCreateView(LoginRequiredMixin,ApplicantRequiredMixin,ApplicantCompleteProfileMixin,CreateView):
    model=Application
    template_name='application/application_create.html'
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


class ApplicationAdmitView(LoginRequiredMixin,EvaluatorOrSecretaryRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):
    model=Application
    form_class=ApplicationAdmitForm
    template_name = 'application/application_admit.html'
    success_message = _('Application admitted !')

    def test_func(self):
        call = Call.objects.get(id=self.kwargs['call_pk'])
        user = self.request.user
        if user.is_evaluator:
            evaluator=user.evaluator
            if evaluator in call.evaluators.all():
                return True
        if user.is_secretary:
            if call.msc_programme.department==user.secretary.department:
                return True
        return False

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['admitted'].label = ""
        form.fields['admitted_flow'].queryset = self.object.preferences.all()
        form.fields['admitted_flow'].label = ""
        return form

    def get_success_url(self):
        return reverse('msc:call_application_list',kwargs={'pk':self.get_object().call.id} )


# MSC Programmes
class MscProgrammeListView(ListView):
    model=MscProgramme
    template_name='msc_programme/msc_programme_list.html'
    context_object_name='programmes'

    def get_queryset(self):
        qs = self.model.objects.all()
        programme_filtered_list = MscProgrammeFilter(self.request.GET, queryset=qs)
        return programme_filtered_list.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = MscProgrammeFilter(self.request.GET, queryset)
        context['filter'] = filter
        return context

class MscProgrammeDetailView(DetailView):
    model=MscProgramme
    template_name='msc_programme/msc_programme_detail.html'
    context_object_name='programme'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calls = Call.objects.filter(Q(end_date__gte=datetime.datetime.now())&Q(start_date__lte=datetime.datetime.now())).filter(msc_programme__id=self.kwargs['pk'])
        context['calls']=calls
        return context

class MSCFlowInline(InlineFormSetFactory):
    model = MscFlow
    form_class=MscFlowForm
    factory_kwargs = {'extra': 1}


class MscProgrammeCreateView(SuccessMessageMixin,SecretaryRequiredMixin,CreateWithInlinesView):
    model=MscProgramme
    form_class=MscProgrammeForm
    inlines = [ MSCFlowInline,]
    template_name='msc_programme/msc_programme_create.html'
    success_message = _('MSC Programme created !')
    success_url=reverse_lazy('secretary:secretary_programmes')

    def form_valid(self, form):
        form.instance.department=self.request.user.secretary.department
        return super().form_valid(form)


class MscProgrammeUpdateView(SuccessMessageMixin,SecretaryRequiredMixin,UpdateWithInlinesView):
    model=MscProgramme
    form_class=MscProgrammeForm
    inlines = [ MSCFlowInline,]
    template_name='msc_programme/msc_programme_update.html'
    success_message = _('MSC Programme updated !')
    success_url=reverse_lazy('secretary:secretary_programmes')

    def test_func(self):
        user = self.request.user
        if user.secretary:
            if self.get_object().department==user.secretary.department:
                return True
        return False

    def form_valid(self, form):
        form.instance.department=self.request.user.secretary.department
        return super().form_valid(form)


class MscProgrammeDeleteView(LoginRequiredMixin,SecretaryRequiredMixin,UserPassesTestMixin,DeleteView):
    model=MscProgramme

    def test_func(self):
        user = self.request.user
        if user.secretary:
            if self.get_object().department==user.secretary.department:
                return True
        return False

    def get_success_url(self):
        messages.success(self.request, (_('MSC Programme deleted.')))
        return reverse('secretary:secretary_programmes')

#Calls
class CallListView(ListView):
    model = Call
    template_name = 'call/call_list.html'
    context_object_name = 'calls'

    def get_queryset(self) :
        queryset = Call.objects.filter(Q(end_date__gte=datetime.datetime.now())&Q(start_date__lte=datetime.datetime.now()))
        return queryset


class CallDetailView(DetailView):
    model = Call
    template_name = 'call/call_detail.html'
    context_object_name = 'call'

class CallCreateView(SuccessMessageMixin,SecretaryRequiredMixin,CreateView):
    template_name='call/call_create.html'
    success_message = _('Call created !')
    success_url=reverse_lazy('secretary:secretary_calls')
    form_class=CallForm

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['evaluators'].queryset = Evaluator.objects.filter(department=self.request.user.secretary.department)
        form.fields['msc_programme'].queryset = MscProgramme.objects.filter(department=self.request.user.secretary.department)
        return form

class CallUpdateView(SuccessMessageMixin,SecretaryRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Call
    form_class=CallForm
    template_name='call/call_update.html'
    success_message = _('Call updated !')
    success_url=reverse_lazy('secretary:secretary_calls')

    def test_func(self):
        user = self.request.user
        if user.secretary:
            if self.get_object().msc_programme.department==user.secretary.department:
                return True
        return False

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['evaluators'].queryset = Evaluator.objects.filter(department=self.request.user.secretary.department)
        form.fields['msc_programme'].queryset = MscProgramme.objects.filter(department=self.request.user.secretary.department)
        return form


class CallDeleteView(LoginRequiredMixin,SecretaryRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Call

    def test_func(self):
        user = self.request.user
        if user.secretary:
            if self.get_object().msc_programme.department==user.secretary.department:
                return True
        return False

    def get_success_url(self):
        messages.success(self.request, (_('Call deleted.')))
        return reverse('secretary:secretary_calls')
