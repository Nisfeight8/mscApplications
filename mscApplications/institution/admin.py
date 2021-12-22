from django.contrib import admin
from .models import *

class DepartmentInline(admin.StackedInline):
    model = Department
    extra = 1

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['title','country','city','address','pobox','telephone' ]
    search_fields = ('title', 'telephone','country','city')
    list_filter = ('country', 'city')
    inlines=[DepartmentInline]

admin.site.register(Institution,InstitutionAdmin)