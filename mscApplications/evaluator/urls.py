from django.urls import  path
from .views import *

app_name = 'evaluator'

urlpatterns = [
    path('home/', EvaluatorHomeView.as_view(), name='evaluator_home'),
    path('profile/', EvaluatorProfileDetailView.as_view(), name='evaluator_profile'),
    path('calls/', EvaluatorCallListView.as_view(),name='evaluator_call'),
    path('profile/edit/', EvaluatorProfileUpdateView.as_view(), name='evaluator_profile_edit'),
]