from .models import User
from evaluator.models import Evaluator
from applicant.models import Applicant
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Permission


@receiver(post_save, sender=User)
def create_applicant(sender, instance, created, *args, **kwargs):
    user = instance
    if created:
        if user.is_applicant:
            Applicant.objects.create(user=user)
        if user.is_staff:
            permissions=list(Permission.objects.filter(codename__in=['view_evaluator','add_evaluator','delete_evaluator','change_evaluator','view_user','add_user','delete_user','change_user','view_call','add_call','delete_call','change_call','view_mscprogramme','add_mscprogramme','delete_mscprogramme','change_mscprogramme','view_mscflow','add_mscflow','delete_mscflow','change_mscflow']))
            user.user_permissions.set(permissions)
    else:
        if user.is_applicant:
            if not Applicant.objects.filter(user_id=user.id).exists():
                Applicant.objects.create(user=user)
