from django.urls import  path
from .views import *

app_name = 'msc'

urlpatterns = [
    path('calls', CallListView.as_view(), name='call_list'),
    path('calls/create', CallCreateView.as_view(), name='call_create'),
    path('calls/<int:pk>/detail', CallDetailView.as_view(), name='call_detail'),
    path('calls/<int:pk>/delete', CallDeleteView.as_view(), name='call_delete'),
    path('calls/<int:pk>/update', CallUpdateView.as_view(), name='call_update'),
    path('calls/<int:pk>/applications', ApplicationListView.as_view(), name='call_application_list'),
    path('calls/<int:pk>/new-application', ApplicationCreateView.as_view(), name='call_new_application'),
    path('calls/<int:call_pk>/applications/<int:pk>/admit', ApplicationAdmitView.as_view(), name='call_application_admit'),
    path('programmes', MscProgrammeListView.as_view(), name='msc_programme_list'),
    path('programmes/create', MscProgrammeCreateView.as_view(), name='msc_programme_create'),
    path('programmes/<int:pk>', MscProgrammeDetailView.as_view(), name='msc_programme_detail'),
    path('programmes/<int:pk>/edit', MscProgrammeUpdateView.as_view(), name='msc_programme_update'),
    path('programmes/<int:pk>/delete', MscProgrammeDeleteView.as_view(), name='msc_programme_delete'),
]