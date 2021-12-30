from django.urls import  path
from .views import *

app_name = 'org'

urlpatterns = [
    path('institutions/<int:pk>/detail/', InstitutionDetailView.as_view(), name='institution_detail'),
    path('departments/<int:pk>/detail/', DepartmentDetailView.as_view(), name='department_detail'),
]
