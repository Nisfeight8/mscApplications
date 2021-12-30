from django.contrib import admin
from .models import *
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

    def get_exclude(self, request,obj) :
        if request.user.is_superuser:
            exclude = super(EvaluatorInline, self).get_exclude(request,obj)
        else:
            exclude=('department',)
        return exclude

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
                     'is_staff', 'is_applicant','is_evaluator')
    list_filter = ('email', 'is_staff', 'is_applicant','is_evaluator',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name',
                           'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_applicant','is_evaluator',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name', 'password1', 'password2', 'is_staff','is_applicant','is_evaluator' , 'is_active')}
         ),
    )
    search_fields = ('last_name', 'email',)
    ordering = ('email',)
    def get_fieldsets(self, request, obj):
        if request.user.is_superuser:
            fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)
        else:
            if obj != None:
                fieldsets = (
                    (None, {'fields': ('first_name', 'last_name',
                            'email', 'password')}),
                )
            else:
                fieldsets = (
                (None, {
                    'classes': ('wide',),
                        'fields': ('email','first_name','last_name', 'password1', 'password2' , 'is_active')}
                ),
            )
        return fieldsets

    def add_view(self, request, form_url='', extra_context=None):
        if request.user.is_superuser:
            self.inlines = []
        else:
            self.inlines =[EvaluatorInline]
        return super().add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_superuser:
            obj = self.model.objects.get(pk=object_id)
            if not obj:
                self.inlines = []
            else:
                if obj.is_applicant:
                    self.inlines = [ApplicantInline]
                if obj.is_evaluator:
                    self.inlines = [EvaluatorInline]
                if obj.is_staff:
                    self.inlines = [SecretaryInline]
        else:
            self.inlines=[EvaluatorInline]
        return super().change_view(request,object_id,form_url=form_url,extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.is_evaluator=True
        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model != Evaluator or request.user.is_superuser:
            return super(UserAdmin, self).save_formset(request, form, formset, change)

        sec=Secretary.objects.get(user_id=request.user.id)
        instances = formset.save(commit=False)
        for instance in instances:
            instance.department=sec.department
            instance.save()
        formset.save_m2m()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            sec=Secretary.objects.get(user_id=request.user.id)
            return User.objects.filter(evaluator__department=sec.department) or qs.none()
        return qs

admin.site.register(User,UserAdmin)

