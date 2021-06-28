from modeltranslation.translator import register , TranslationOptions
from .models import *

@register(MscProgramme)
class MscProgrammeTranslationOptions(TranslationOptions):
    fields = ('title', 'address','city','country')

@register(MscFlow)
class MscFlowTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Call)
class CallTranslationOptions(TranslationOptions):
    fields = ('title',)

