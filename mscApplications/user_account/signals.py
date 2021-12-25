from .models import User
from evaluator.models import Evaluator
from applicant.models import Applicant
from django.dispatch import receiver
from django.db.models.signals import post_save



@receiver(post_save, sender=User)
def create_applicant(sender, instance, created, *args, **kwargs):
    user = instance
    if created:
        if user.is_applicant:
            Applicant.objects.create(user=user)
    else:
        if user.is_applicant:
            if not Applicant.objects.filter(user_id=user.id).exists():
                Applicant.objects.create(user=user)
