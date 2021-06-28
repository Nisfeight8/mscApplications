from django.urls import include, path
from .views import *

app_name = 'evaluator'

urlpatterns = [
    path('home/', EvaluatorHomeView.as_view(), name='evaluator_home'),
    path('profile/', ProfileDetailView.as_view(), name='evaluator_profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='evaluator_profile_edit'),
    path('applications/', CallDetailView.as_view(), name='call_applications'),
    path('applications/<int:pk>/', ApplicationAdmitView.as_view(), name='application_update'),
    path('applications/applicant/<int:pk>/', ApplicantDetailView.as_view(), name='applicant_detail'),
]