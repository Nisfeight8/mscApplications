from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin,TranslationStackedInline


class DepartmentInline(TranslationStackedInline):
    model = Department
    extra = 1

class InstitutionAdmin(TranslationAdmin):
    list_display = ['title','country','city','address','pobox','telephone' ]
    search_fields = ('title', 'telephone','country','city')
    list_filter = ('country', 'city')
    inlines=[DepartmentInline]

admin.site.register(Institution,InstitutionAdmin)