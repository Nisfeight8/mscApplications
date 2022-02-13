from django.contrib import admin
from .models import *
from msc.models import Preference,Application

class DiplomaInline(admin.StackedInline):
    model = Diploma
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    extra = 0
    verbose_name_plural = 'diploma'


class PhdInline(admin.StackedInline):
    model = Phd
    extra = 0
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    can_delete = False
    verbose_name_plural = 'phd'


class JobExperienceInline(admin.StackedInline):
    model = JobExperience
    can_delete = False
    extra = 0
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    verbose_name_plural = 'jobExperience'


class ReferenceInline(admin.StackedInline):
    model = Reference
    extra = 0
    can_change= False
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    verbose_name_plural = 'reference'


class ApplicantAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    inlines = [ ReferenceInline, JobExperienceInline,PhdInline,DiplomaInline ]
    readonly_fields = ('user','telephone','address','city','birth_date','gender','citizenship','country',)
    list_display = ['user','telephone','address','city','country','birth_date','gender','citizenship']


class PreferenceInline(admin.StackedInline):
    model = Preference
    extra = 0
    def has_change_permission(self, request, obj=None):
        return True
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    readonly_fields = ('priority','flow',)
    verbose_name_plural = 'preference'


class ApplicationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False
    def get_form(self, request, obj=None, **kwargs):
        form = super(ApplicationAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['admitted_flow'].queryset = obj.preferences.all()
        return form
    inlines = [ PreferenceInline, ]
    readonly_fields = ('applicant','comments','submission_date','call','reference','media_file')
    list_display = ['applicant','comments','submission_date','call','reference','media_file','admitted','admitted_flow' ]
    verbose_name_plural = 'application'

admin.site.register(Applicant,ApplicantAdmin)

admin.site.register(Application,ApplicationAdmin)


admin.site.site_header = 'MSC Applications Administration'
admin.site.index_title = 'MSC Applications administration'
admin.site.site_title = 'Welcome Admin'

