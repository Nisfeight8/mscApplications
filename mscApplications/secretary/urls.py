from django.urls import  path
from .views import *

app_name = 'secretary'

urlpatterns = [
    path('dashboard/', SecretaryDashboard.as_view(), name='secretary_dashboard'),
]