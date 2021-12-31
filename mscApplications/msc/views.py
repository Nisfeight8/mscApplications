from .models import *
from django.db.models import Q
from django.views.generic import ListView,DetailView
from applicant.models import Application
import datetime
from utils.mixins import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from .filters import MscProgrammeFilter
from django.utils.translation import get_language

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

