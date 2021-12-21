from django.conf.urls import url
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'user_account'


urlpatterns = [

    path('',
    Home.as_view(),
    name='home'),

    path(
    'login/',
    auth_views.LoginView.as_view(redirect_authenticated_user= True,
    template_name='login.html'), name='login'),

    path('logout/',
    auth_views.LogoutView.as_view(),
    name='logout'),

    # Change Password
    path(
    'change-password/',
    auth_views.PasswordChangeView.as_view(
    template_name='change-password.html',
    success_url = '/login'
    ),
    name='change_password'
    ),
    path(
    'user-change-password/',
    ChangePasswordView.as_view(),
    name='user_change_password'
    ),
    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password-reset/password_reset.html',
             subject_template_name='password-reset/password_reset_subject.txt',
             email_template_name='password-reset/password_reset_email.html',
             success_url='/password-reset/done/'
         ),
         name='password_reset'),
    path('password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
    template_name='password-reset/password_reset_done.html'
    ),
    name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
    template_name='password-reset/password_reset_confirm.html',
     success_url='/password-reset-complete/'
    ),
    name='password_reset_confirm'),

    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
    template_name='password-reset/password_reset_complete.html'
    ),
    name='password_reset_complete'),

    path('signup/complete',ApplicantCreateView.as_view(),name='new_applicant'),

]