from django.contrib import admin
from .models import *
from secretary.models import Secretary
from evaluator.models import Evaluator
from applicant.models import Applicant
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group


admin.site.unregister(Group)

# Register your models here.
class EvaluatorInline(admin.StackedInline):
    model = Evaluator
    can_delete = True
    verbose_name_plural = 'evaluator'


class ApplicantInline(admin.StackedInline):
    model = Applicant
    can_delete = True
    verbose_name_plural = 'applicant'

class SecretaryInline(admin.StackedInline):
    model = Secretary
    can_delete = True
    verbose_name_plural = 'secretary'

class UserAdmin(UserAdmin):
    list_per_page = 10
    model = User
    list_display = ('email','first_name', 'last_name',
                     'is_staff','is_secretary', 'is_applicant','is_evaluator')
    list_filter = ('email', 'is_staff','is_secretary', 'is_applicant','is_evaluator',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name',
                           'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_secretary','is_applicant','is_evaluator',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name', 'password1', 'password2', 'is_staff','is_secretary','is_applicant','is_evaluator' , 'is_active')}
         ),
    )
    search_fields = ('last_name', 'email',)
    ordering = ('email',)
    

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        
        obj = self.model.objects.get(pk=object_id)
        if not obj:
            self.inlines = []
        else:
            if obj.is_applicant:
                self.inlines = [ApplicantInline]
            if obj.is_evaluator:
                self.inlines = [EvaluatorInline]
            if obj.is_secretary:
                self.inlines = [SecretaryInline]
        
        return super().change_view(request,object_id,form_url=form_url,extra_context=extra_context)


admin.site.register(User,UserAdmin)

