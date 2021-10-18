"""mscApplications URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from decorator_include import decorator_include
from django.contrib.auth.decorators import login_required
from utils import decorators
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('', include('user_account.urls',namespace='user_account')),
    path('applicant/', decorator_include([login_required,decorators.group_required('applicant')],'applicant.urls',namespace='applicant')),
    path('evaluator/', decorator_include([login_required,decorators.group_required('evaluator')],'evaluator.urls',namespace='evaluator')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django_translation_flags.urls'))
]
if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)