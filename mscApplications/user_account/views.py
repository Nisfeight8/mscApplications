from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView,View,FormView
from django.shortcuts import redirect
from .forms import *
from applicant.models import *

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _

class CheckUser(View):
    def get(self,request):
        if self.request.user.is_authenticated:
            user=self.request.user
            if user.is_applicant:
                applicant=user.applicant
                if (applicant.telephone and applicant.birth_date and applicant.address and applicant.city and applicant.country and applicant.citizenship):
                    return redirect('applicant:applicant_home')
                else:
                    return redirect('applicant:applicant_profile_edit')
            elif user.is_evaluator:
                return redirect('evaluator:evaluator_home')
            else:
                user.is_applicant=True
                user.save()
                return redirect('applicant:applicant_profile_edit')
        return redirect('/accounts/login')

class ChangePasswordView(LoginRequiredMixin,FormView):
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
        if self.request.user.is_applicant:
            return redirect('applicant:applicant_profile')
        if self.request.user.is_evaluator:
            return redirect('evaluator:evaluator_profile')

