from django.contrib import admin
from django.apps import apps
from .models import *

class MscFlowInline(admin.StackedInline):
    model = MscFlow
    extra = 0
    can_delete = True
    verbose_name_plural = 'Flow'
class MscProgrammeAdmin(admin.ModelAdmin):
   inlines=[MscFlowInline]
   list_display = ['title','telephone','address','city','country','department']

admin.site.register(MscProgramme,MscProgrammeAdmin)

admin.site.register(Call)
admin.site.register(Evaluator)

