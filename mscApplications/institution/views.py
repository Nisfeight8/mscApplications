from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.views.generic import ListView,DetailView

class InstitutionDetailView(DetailView):
    model=Institution
    template_name='institution_detail.html'
    context_object_name='institution'


class DepartmentDetailView(DetailView):
    model=Department
    template_name='department_detail.html'
    context_object_name='department'