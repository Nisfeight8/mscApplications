from django.contrib import admin
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


class CallAdmin(admin.ModelAdmin):
   list_display = ['title','start_date','end_date','msc_programme']
admin.site.register(Call,CallAdmin)

