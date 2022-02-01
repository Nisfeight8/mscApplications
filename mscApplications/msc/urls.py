from django.urls import  path
from .views import *

app_name = 'msc'

urlpatterns = [
    path('calls/', CallListView.as_view(), name='call_list'),
    path('calls/<int:pk>/detail/', CallDetailView.as_view(), name='call_detail'),
    path('calls/<int:pk>/applications/', CallApplicationListView.as_view(), name='call_application_list'),
    path('calls/<int:pk>/new-application/', CallApplicationCreateView.as_view(), name='call_new_application'),
    path('<int:pk>/admit/', CallApplicationAdmitView.as_view(), name='call_application_admit'),
    path('programmes/', MscProgrammeListView.as_view(), name='msc_programme_list'),
    path('programmes/<int:pk>/', MscProgrammeDetailView.as_view(), name='msc_programme_detail'),
    path('programmes/create/', MscProgrammeCreateView.as_view(), name='msc_programme_create'),
]