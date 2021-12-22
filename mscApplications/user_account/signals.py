from django.contrib.auth.models import Group
from evaluator.models import Evaluator
from applicant.models import Applicant
from django.dispatch import receiver
from django.db.models.signals import post_save



@receiver(post_save, sender=Evaluator)
def evaluator_field_to_user(sender, instance, created, *args, **kwargs):
    evaluator = instance
    if created:
        user=evaluator.user
        user.is_evaluator=True
        user.save()


@receiver(post_save, sender=Applicant)
def applicant_field_to_user(sender, instance, created, *args, **kwargs):
    applicant = instance
    if created:
        user=applicant.user
        user.is_applicant=True
        user.save()
