from django.urls import include, path
from .views import *

app_name = 'applicant'
urlpatterns = [
    path('home/', ApplicantHomeView.as_view(), name='applicant_home'),
    path('profile/', ApplicantProfileDetailView.as_view(), name='applicant_profile'),
    path('profile/edit/', ApplicantProfileUpdateView.as_view(), name='applicant_profile_edit'),
    path('<int:pk>/new-application/', ApplicationCreateView.as_view(), name='new_application'),
    path('<int:pk>/detail/', ApplicantDetailView.as_view(), name='applicant_detail'),
    path('applications/<int:pk>/admit/', ApplicationAdmitView.as_view(), name='application_admit'),
    path('applications/', ApplicantApplicationListView.as_view(), name='applicant_applications'),
]