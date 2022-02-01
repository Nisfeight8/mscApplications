from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin,TranslationStackedInline

class MscFlowInline(TranslationStackedInline):
    model = MscFlow
    extra = 0
    can_delete = True
    verbose_name_plural = 'Flow'

class MscProgrammeAdmin(TranslationAdmin):
   inlines=[MscFlowInline]
   list_display = ['title','telephone','address','city','country','department']

   
admin.site.register(MscProgramme,MscProgrammeAdmin)

class CallAdmin(TranslationAdmin):
   list_display = ['title','start_date','end_date','msc_programme']
   
admin.site.register(Call,CallAdmin)

