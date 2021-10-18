from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView,View,UpdateView,FormView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import views as auth_views
from applicant_degrees.models import Applicant
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

class UserSignUpView(CreateView):
    model=User
    form_class=UserSignUpForm
    template_name = 'signup.html'
    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()
        current_site = self.request.META['HTTP_HOST']
        email_subject = 'Activate Your Account'
        message = render_to_string('activate_account.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        messages.success(self.request, ('Please Confirm your email to complete registration.'))
        return redirect('user_account:login')
class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account has been confirmed.'))
            return redirect('user_account:new_applicant')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
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

class ChangeEmailView(UpdateView,LoginRequiredMixin):
    model=User
    form_class = EmailChangeForm
    template_name = 'user-change-email.html'
    def form_valid(self, form):
        user = form.save(commit=False)
        print(user)
        user.email=form.cleaned_data['new_email']
        user.save()
        messages.success(self.request, _('Your email was successfully updated!'))
        if self.request.user.groups.filter(name='applicant').exists():
            return redirect('applicant:applicant_profile')
        if self.request.user.groups.filter(name='evaluator').exists():
            return redirect('evaluator:evaluator_profile')
    def get_object(self,queryset=None):
        return self.request.user

