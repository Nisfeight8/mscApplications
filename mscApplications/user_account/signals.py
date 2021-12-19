from django.contrib.auth.models import Group
from msc.models import Evaluator
from applicant_degrees.models import Applicant
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import Group,Permission
from.models import *


@receiver(post_save, sender=Evaluator)
def evaluator_field_to_user(sender, created, instance, **kwargs):
    evaluator = instance
    if created:
        evaluator.user.is_evaluator=True

@receiver(post_save, sender=Applicant())
def applicant_field_to_user(sender, created, instance, **kwargs):
    applicant = instance
    if created:
        applicant.user.is_applicant=True
