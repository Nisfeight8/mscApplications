from django.views.generic import DetailView, UpdateView,View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from institution.models import Department
# Create your views here.

class SecretaryDashboard(LoginRequiredMixin,TemplateView):
    template_name = 'secretary_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super(SecretaryDashboard, self).get_context_data(**kwargs)
        context['department']=self.request.user.secretary.department
        return context

