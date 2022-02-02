from django.conf.urls import url
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

app_name = "user_account"


urlpatterns = [
    path("check", CheckUser.as_view(), name="check-user"),
    path("change-password", ChangePasswordView.as_view(), name="user_change_password"),
]
