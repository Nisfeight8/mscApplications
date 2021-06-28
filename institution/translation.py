from modeltranslation.translator import register, TranslationOptions
from .models import *

@register(Institution)
class InstitutionTranslationOptions(TranslationOptions):
    fields = ('title', 'address','city','country')

@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('title', 'address','city','country')


