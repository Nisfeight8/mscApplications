import django_filters
from .models import MscProgramme


class MscProgrammeFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = MscProgramme
        fields = ['title','department__country','department__city','department']

