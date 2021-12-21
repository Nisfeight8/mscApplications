from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from evaluator.models import Evaluator
from applicant.models import Applicant
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.
class EvaluatorInline(admin.StackedInline):
    model = Evaluator
    can_delete = True
    verbose_name_plural = 'evaluator'
class ApplicantInline(admin.StackedInline):
    model = Applicant
    can_delete = True
    verbose_name_plural = 'applicant'
