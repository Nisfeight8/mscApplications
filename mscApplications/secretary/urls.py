from django.urls import  path
from .views import *

app_name = 'secretary'

urlpatterns = [
    path('home', SecretaryHome.as_view(), name='secretary_home'),
     path('profile', SecretaryProfileDetailView.as_view(), name='secretary_profile'),
    path('profile/edit', SecretaryProfileUpdateView.as_view(), name='secretary_profile_edit'),
    path('calls', SecretaryCallListView.as_view(), name='secretary_calls'),
    path('programmes', SecretaryMscProgrammeListView.as_view(), name='secretary_programmes'),
    path('evaluators', SecretaryEvaluatorListView.as_view(), name='secretary_evaluators'),
]