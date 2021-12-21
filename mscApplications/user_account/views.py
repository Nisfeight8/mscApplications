from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView,View,FormView
from django.shortcuts import redirect
from .forms import *
from applicant.models import *
from applicant.forms import *

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _

class Home(View):
    def get(self,request):
        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='applicant').exists():
                return redirect('applicant:applicant_home')
            elif self.request.user.groups.filter(name='evaluator').exists():
                return redirect('evaluator:evaluator_home')
            elif self.request.user.is_superuser:
                return HttpResponseRedirect(reverse('admin:index'))
            else:
               return redirect('user_account:new_applicant')
        return redirect('user_account:login')


class ApplicantCreateView(LoginRequiredMixin,CreateView):
    model=Applicant
    form_class=ApplicantForm
    template_name = 'new-applicant.html'
    def form_valid(self, form):
        applicant = form.save(commit=False)
        self.request.user.first_name=form.cleaned_data['first_name']
        self.request.user.last_name=form.cleaned_data['last_name']
        self.request.user.save()
        applicant.user=self.request.user
        applicant.save()
        return redirect('applicant:applicant_profile')

class ChangePasswordView(FormView,LoginRequiredMixin):
    model=User
    form_class = PasswordChangeForm
    template_name = 'user-change-password.html'
    def get_form_kwargs(self):
        kwargs = super(ChangePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)  # Important!
        messages.success(self.request, _('Your password was successfully updated!'))
        if self.request.user.groups.filter(name='applicant').exists():
            return redirect('applicant:applicant_profile')
        if self.request.user.groups.filter(name='evaluator').exists():
            return redirect('evaluator:evaluator_profile')

