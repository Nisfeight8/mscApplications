from django.db import models
from institution.models import Department
from django.utils.translation import gettext as _
from evaluator.models import Evaluator
from django.db import models
from applicant.models import Applicant,Reference
from .utils import application_upload
from django.core.validators import FileExtensionValidator

class MscProgramme(models.Model):
    title = models.CharField(_('Title'),max_length = 200)
    address = models.CharField(_('Address'),max_length=50)
    description=models.TextField(_('description'),null=True,blank=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE, verbose_name=_("Department"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("MSC Programme")
        verbose_name_plural = _("MSC Programmes")

class MscFlow(models.Model):
    title = models.CharField(_('Title'),max_length = 200)
    msc_programme=models.ForeignKey(MscProgramme,on_delete=models.CASCADE,verbose_name=_("Msc Programme"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("MSC Flow")
        verbose_name_plural = _("MSC Flows")


class Call(models.Model):
    title = models.CharField(_('Title'),max_length = 200)
    start_date=models.DateField(_('Start date'))
    end_date=models.DateField(_('End Date'))
    msc_programme=models.ForeignKey(MscProgramme,on_delete=models.CASCADE, verbose_name=_("Msc Programme"))
    evaluators = models.ManyToManyField(
        Evaluator, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Call")
        verbose_name_plural = _("Calls")

class Application (models.Model):
    applicant=models.ForeignKey(Applicant,on_delete=models.CASCADE)
    call=models.ForeignKey(Call,on_delete=models.CASCADE)
    submission_date=models.DateField(_('Submission Date'),auto_now_add=True)
    comments=models.TextField(_('Comments'),null=True,blank=True)
    admitted=models.BooleanField(_('Admitted'),default=None,null=True,blank=True)
    reference=models.ForeignKey(Reference,on_delete=models.SET_NULL,null=True,blank=True)
    media_file = models.FileField(_('Media File'),upload_to=application_upload,validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    preferences = models.ManyToManyField(MscFlow,through='Preference',blank=True,related_name="waiting_applications")
    admitted_flow=models.ForeignKey(MscFlow,on_delete=models.CASCADE,blank=True,null=True,related_name="admitted_application")

    def __str__(self):
        return self.applicant.user.email+" application"

    class Meta:
        verbose_name = _("Application")
        verbose_name_plural = _("Applications")
        constraints = [
        models.UniqueConstraint(fields=['applicant', 'call'], name='unique call for applicant')
    ]
class Preference(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    flow = models.ForeignKey(MscFlow,on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(_('Priority'),)

    class Meta:
        ordering = ["priority"]
        verbose_name = _("Priority")
        verbose_name_plural = _("Priorities")

    def __str__(self):
        return  self.flow.title