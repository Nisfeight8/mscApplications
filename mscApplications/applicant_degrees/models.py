from django.db import models
from msc.models import Call,MscFlow
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


def only_int(value):
    if value.isdigit()==False:
        raise ValidationError(_('Only digits allowed'))
    elif len(value)<10:
        raise ValidationError(_('Telephone must have 10 digits'))


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='applicant',primary_key=True, verbose_name=_("User"))
    telephone = models.CharField(_('Telephone'),max_length = 10,validators=[only_int])
    address = models.CharField(_('Address'),max_length=50)
    city = models.CharField(_('City'),max_length=64)
    country = models.CharField(_('Country'),max_length=50)
    birth_date=models.DateField()
    MALE='M'
    FEMALE='F'
    GENDER_CHOICES = [
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    ]
    gender = models.CharField(_('Gender'),max_length=1, choices=GENDER_CHOICES)
    citizenship = models.CharField(_('Citizenship'),max_length=64)
    def __str__(self):
        try:
            return self.user.first_name+" "+self.user.last_name
        except ObjectDoesNotExist:
            return self.telephone
class Diploma (models.Model):
    UNDERGRADUATE='UG'
    POSTGRADUATE='PG'
    TYPE_CHOICES = [
        (UNDERGRADUATE, _('Undergraduate')),
        (POSTGRADUATE, _('Postgraduate')),
    ]
    type = models.CharField(_('Type'),max_length=2, choices=TYPE_CHOICES)
    awarding_institution=models.CharField(_('Awarding Institution'),max_length=200)
    department=models.CharField(_('Department'),max_length=200)
    specialization=models.CharField(_('Specialization'),max_length=100,blank=True,null=True)
    date_awarded=models.DateField(_('Date Awarded'),)
    grade_point_average=models.CharField(_('Average Grade'),max_length=2)
    city = models.CharField(_('City'),max_length=64)
    country = models.CharField(_('Country'),max_length=50)
    media_file = models.FileField(_('Media File'),validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    applicant=models.ForeignKey(Applicant,on_delete=models.CASCADE ,verbose_name=_("Applicant"))
    def __str__(self):
        return self.awarding_institution

class Phd(models.Model):
    UNDERGRADUATE='UG'
    POSTGRADUATE='PG'
    TYPE_CHOICES = [
        (UNDERGRADUATE, _('Undergraduate')),
        (POSTGRADUATE, _('Postgraduate')),
    ]
    type = models.CharField(_('Type'),max_length=2, choices=TYPE_CHOICES)
    awarding_institution=models.CharField(_('Awarding Institution'),max_length=200)
    department=models.CharField(_('Department'),max_length=200)
    title = models.CharField(_('Title'),max_length = 200)
    supervisor=models.CharField(_('Supervisor'),max_length=64)
    date_awarded=models.DateField(verbose_name=_('Date Awarded'),)
    grade_point_average=models.CharField(_('Average Grade'),max_length=2)
    city = models.CharField(_('City'),max_length=64)
    country = models.CharField(_('Country'),max_length=50)
    media_file = models.FileField(verbose_name=_('Media File'),validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    applicant=models.ForeignKey(Applicant,on_delete=models.CASCADE,verbose_name=_("Applicant"))
    def __str__(self):
        return self.title
class JobExperience (models.Model):
    organization=models.CharField(_('Organization'),max_length=200)
    city = models.CharField(_('City'),max_length=64)
    country = models.CharField(_('Country'),max_length=50)
    job_title = models.CharField(_('Job Title'),max_length = 200)
    start_date=models.DateField(_('Start Date'),)
    end_date=models.DateField(verbose_name=_('End Date'),null=True,blank=True)
    media_file = models.FileField(verbose_name=_('Media File'),validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    applicant=models.ForeignKey(Applicant,on_delete=models.CASCADE,verbose_name=_("Applicant"))
    def __str__(self):
        return self.job_title
class Reference (models.Model):
    organization=models.CharField(_('Organization'),max_length=200)
    city = models.CharField(_('City'),max_length=64)
    country = models.CharField(_('Country'),max_length=50)
    job_title = models.CharField(_('Job Title'),max_length = 200)#job title of the guy who gives the reference
    first_name=models.CharField(_('First Name'),max_length = 30)#first name of the guy who gives the reference
    last_name=models.CharField(_('Last Name'),max_length=50)#last name of the guy who gives the reference
    telephone = models.CharField(_('Telephone'),max_length = 10)
    reference_date=models.DateField(verbose_name=_('Reference Date'),)
    media_file = models.FileField(verbose_name=_('Media File'),validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    applicant=models.ForeignKey(Applicant,on_delete=models.CASCADE,verbose_name=_("Applicant"))
    def __str__(self):
        return self.job_title


class Application (models.Model):
    applicant=models.ForeignKey(Applicant,on_delete=models.CASCADE)
    call=models.ForeignKey(Call,on_delete=models.CASCADE)
    submission_date=models.DateField(verbose_name=_('Submission Date'),auto_now_add=True)
    comments=models.TextField(_('Comments'),null=True,blank=True)
    admitted=models.BooleanField(_('Admitted'),default=None,null=True,blank=True)
    reference=models.ForeignKey(Reference,on_delete=models.SET_NULL,null=True,blank=True,verbose_name=_("Reference"))
    media_file = models.FileField(verbose_name=_('Media File'),validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    preferences = models.ManyToManyField(MscFlow,through='Preference',blank=True,related_name="waiting_applications",verbose_name=_("Preferences"))
    admitted_flow=models.ForeignKey(MscFlow,on_delete=models.CASCADE,blank=True,null=True,related_name="admitted_application",verbose_name=_("Admitted FLow"))
    def __str__(self):
        return self.applicant.user.username+" application"
class Preference(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE,verbose_name=_("Application"))
    flow = models.ForeignKey(MscFlow,on_delete=models.CASCADE,verbose_name=_("Flow"))
    priority = models.PositiveIntegerField(_('Priority'),)
    class Meta:
        ordering = ["priority"]
    def __str__(self):
        return  self.flow.title
