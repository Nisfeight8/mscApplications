from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin,TranslationStackedInline
from user_account.models import Secretary
from django import forms


class MscFlowInline(TranslationStackedInline):
    model = MscFlow
    extra = 0
    can_delete = True
    verbose_name_plural = 'Flow'

class MscProgrammeAdmin(TranslationAdmin):
   inlines=[MscFlowInline]
   list_display = ['title','telephone','address','city','country','department']

   def get_readonly_fields(self, request, obj=None):
      if not request.user.is_superuser:
         return ['department']
      else:
         return []
   def save_model(self, request, obj, form, change):
      if not request.user.is_superuser:
         sec=Secretary.objects.get(user_id=request.user.id)
         obj.department=sec.department
      obj.save()

   def get_queryset(self, request):
      qs = super().get_queryset(request)
      if not request.user.is_superuser:
         sec=Secretary.objects.get(user_id=request.user.id)
         return MscProgramme.objects.filter(department=sec.department) or qs.none()
      return qs


admin.site.register(MscProgramme,MscProgrammeAdmin)


class CallAdmin(TranslationAdmin):
   list_display = ['title','start_date','end_date','msc_programme']
   def get_form(self, request, obj=None, **kwargs):
         form = super(CallAdmin, self).get_form(request, obj, **kwargs)
         if not request.user.is_superuser:
            sec=Secretary.objects.get(user_id=request.user.id)
            form.base_fields['msc_programme'].queryset = MscProgramme.objects.filter(department=sec.department)
            form.base_fields['evaluators'].queryset = Evaluator.objects.filter(department=sec.department)
         return form
   def get_queryset(self, request):
      qs = super().get_queryset(request)
      if not request.user.is_superuser:
         sec=Secretary.objects.get(user_id=request.user.id)
         return Call.objects.filter(msc_programme__department=sec.department) or qs.none()
      return qs
admin.site.register(Call,CallAdmin)

