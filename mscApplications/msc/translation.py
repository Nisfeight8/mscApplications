from modeltranslation.translator import translator, TranslationOptions
from .models import *

class MscProgrammeTranslationOptions(TranslationOptions):
    fields = ('title', 'address','city','country')

translator.register(MscProgramme, MscProgrammeTranslationOptions)


class MscFlowTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(MscFlow, MscFlowTranslationOptions)


class CallTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(Call, CallTranslationOptions)
