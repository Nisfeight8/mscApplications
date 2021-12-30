from modeltranslation.translator import translator, TranslationOptions
from .models import *

class InstitutionTranslationOptions(TranslationOptions):
    fields = ('title', 'address','city','country')

translator.register(Institution, InstitutionTranslationOptions)

class DepartmentTranslationOptions(TranslationOptions):
    fields = ('title', 'address','city','country')

translator.register(Department, DepartmentTranslationOptions)
