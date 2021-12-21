from django.urls import include, path
from .views import *

app_name = 'applicant'

urlpatterns = [
    path('home/', ApplicantHomeView.as_view(), name='applicant_home'),
    path('profile/', ApplicantProfileDetailView.as_view(), name='applicant_profile'),
    path('profile/edit/', ApplicantProfileUpdateView.as_view(), name='applicant_profile_edit'),
    path('calls/', OpenCallListView.as_view(), name='calls'),
    path('calls/<int:pk>/', OpenCallDetailView.as_view(), name='call_detail'),
    path('calls/<int:pk>/application-new', ApplicationCreateView.as_view(), name='new_application'),
]