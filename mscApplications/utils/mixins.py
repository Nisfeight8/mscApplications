from applicant.models import Applicant
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

class ApplicantCompleteProfileMixin:

    def dispatch(self, request, *args, **kwargs):
        user=request.user
        applicant=get_object_or_404(Applicant, user_id=user.id)
        if (not applicant.telephone and not applicant.birth_date and not applicant.address and not applicant.city and not applicant.country and not applicant.citizenship):
            messages.warning(request, _('You need to update your profile first ! We need some extra informations about you !'))
            return redirect('/applicant/profile/edit?next=/applicant/calls/'+str(self.kwargs['pk'])+'/application-new')
        if (not applicant.reference_set.all() and not applicant.diploma_set.all() and not applicant.phd_set.all() and not applicant.jobexperience_set.all()):
            messages.warning(request, _('You need to add some documents to your profile first !'))
            return redirect('/applicant/profile/edit?next=/applicant/calls/'+str(self.kwargs['pk'])+'/application-new')
        else:
            return super().dispatch(request, *args, **kwargs)
