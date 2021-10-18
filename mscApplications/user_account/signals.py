from django.contrib.auth.models import Group
from msc.models import Evaluator
from applicant_degrees.models import Applicant
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import Group,Permission

@receiver(post_save, sender=Evaluator)
def evaluator_add_to_default_group(sender, **kwargs):
    evaluator = kwargs["instance"]
    if kwargs["created"]:
        evaluatorGroup, created = Group.objects.get_or_create(name='evaluator')
        if created ==True:
            permissions=list(Permission.objects.filter(codename__in=['view_application','change_evaluator','change_application','view_applicant','view_jobexperience','view_diploma','view_phd','view_reference','view_call','view_mscprogramme','view_department','view_institution','view_mscflow']))
            evaluatorGroup.permissions.set(permissions)
            evaluatorGroup.save()
        evaluator.user.groups.add(evaluatorGroup)

@receiver(post_delete, sender=Evaluator)
def applicant_remove_from_default_group(sender, **kwargs):
    evaluator = kwargs["instance"]
    if evaluator.user.groups.filter(name='evaluator').exists():
        evaluator.user.groups.remove(evaluator.user.groups.get(name='evaluator'))
    evaluator.user=None
@receiver(post_save, sender=Applicant)
def applicant_add_to_default_group(sender, **kwargs):
    applicant = kwargs["instance"]
    if kwargs["created"]:
        applicantGroup, created = Group.objects.get_or_create(name='applicant')
        if created ==True:
            permissions=list(Permission.objects.filter(content_type_id__in=[14,17,16,15]) | Permission.objects.filter(codename__in=['view_call','change_applicant','view_application','add_application','view_mscprogramme','view_department','view_institution','view_mscflow']))
            applicantGroup.permissions.set(permissions)
            applicantGroup.save()
        applicant.user.groups.add(applicantGroup)

@receiver(post_delete, sender=Applicant)
def applicant_remove_from_default_group(sender, **kwargs):
    applicant = kwargs["instance"]
    if applicant.user.groups.filter(name='applicant').exists():
        applicant.user.groups.remove(applicant.user.groups.get(name='applicant'))
