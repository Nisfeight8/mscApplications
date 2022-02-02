from django.db.models import Q
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
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


class CallApplicationListView(LoginRequiredMixin,EvaluatorRequiredMixin,ListView):
    model=Application
    template_name= 'call_applications.html'
    context_object_name='applications'

    def get_queryset(self):
        call = Call.objects.get(id=self.kwargs['pk'])
        applications= Application.objects.filter(call=call).order_by('-submission_date')
        return applications

    def get_context_data(self, **kwargs):
        context = super(CallApplicationListView, self).get_context_data(**kwargs)
        context['call']=Call.objects.get(id=self.kwargs['pk'])
        return context


class CallApplicationCreateView(LoginRequiredMixin,ApplicantRequiredMixin,ApplicantCompleteProfileMixin,CreateView):
    model=Application
    template_name='application_create.html'
    form_class=ApplicationForm

    def get_context_data(self, **kwargs):
        context = super(CallApplicationCreateView, self).get_context_data(**kwargs)
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


class CallApplicationAdmitView(LoginRequiredMixin,EvaluatorRequiredMixin,SuccessMessageMixin,UpdateView):
    model=Application
    form_class=ApplicationAdmitForm
    template_name = 'application_admit.html'
    success_message = _('Application admitted !')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['admitted'].label = ""
        form.fields['admitted_flow'].queryset = self.object.preferences.all()
        form.fields['admitted_flow'].label = ""
        return form

    def get_success_url(self):
        return reverse('msc:call_application_list',kwargs={'pk':self.get_object().call.id} )

class MscProgrammeListView(ListView):
    model=MscProgramme
    template_name='msc_programme_list.html'
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
    template_name='msc_programme_detail.html'
    context_object_name='programme'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calls=Call.objects.filter(msc_programme__id=self.kwargs['pk'])
        context['calls']=calls
        return context

class MSCFlowInline(InlineFormSetFactory):
    model = MscFlow
    fields=['title_en','title_el']
    factory_kwargs = {'extra': 1}


class MscProgrammeCreateView(SuccessMessageMixin,CreateWithInlinesView):
    model=MscProgramme
    fields=['title_en','title_el','country_en','country_el','city_en','city_el','address_en','address_el','pobox','telephone']
    inlines = [ MSCFlowInline,]
    template_name='msc_programme_create.html'
    success_message = _('MSC Programme created !')
    success_url='/secretary/dashboard'

    def form_valid(self, form):
        form.instance.department=self.request.user.secretary.department
        return super().form_valid(form)


class MscProgrammeUpdateView(SuccessMessageMixin,UpdateWithInlinesView):
    model=MscProgramme
    fields=['title_en','title_el','country_en','country_el','city_en','city_el','address_en','address_el','pobox','telephone']
    inlines = [ MSCFlowInline,]
    template_name='msc_programme_create.html'
    success_message = _('MSC Programme updated !')
    success_url='/secretary/dashboard'

    def form_valid(self, form):
        form.instance.department=self.request.user.secretary.department
        return super().form_valid(form)


class MscProgrammeDeleteView(DeleteView):
    model=MscProgramme

    def get_success_url(self):
        messages.success(self.request, (_('MSC Programme deleted.')))
        return reverse('secretary:secretary_dashboard')

class MscProgrammeCallListView(ListView):
    model=Call
    template_name='msc_programme_call_list.html'
    context_object_name='calls'

    def get_queryset(self):
        programme=MscProgramme.objects.get(id=self.kwargs.get('pk'))
        return Call.objects.filter(msc_programme=programme)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calls=Call.objects.filter(msc_programme__id=self.kwargs['pk'])
        context['programme']=MscProgramme.objects.get(id=self.kwargs.get('pk'))
        context['calls']= self.get_queryset()
        return context