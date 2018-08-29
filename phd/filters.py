from phd.models import *
from shared.models import *
import django_filters
from django_filters.widgets import LinkWidget
from django_select2.forms import *
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django.db.models import Q #allows for complex queries

class PHDBachelorPOSFilter(django_filters.FilterSet):
    # '''filter for MSCoursePOS items'''
    first = django_filters.CharFilter(method='filter_first_name', label='First Name')
    second = django_filters.CharFilter(method='filter_second_name', label = 'Last Name')
    #ADD NETID TO FILTER

    class Meta:
        model = PHDBachelorPOS
        fields = ()

    #Case Insensitive Filtering to check if search terms contain typed letters AND forms are Approved or Rejected by DGS
    def filter_first_name(self, queryset, name, value):
        return queryset.filter(Q(owner__first_name__icontains=value))

    def filter_second_name(self, queryset, name, value):
        return queryset.filter(Q(owner__last_name__icontains=value))


class PHDMasterPOSFilter(django_filters.FilterSet):
    # '''filter for MSProjectPOS items'''
    first = django_filters.CharFilter(method='filter_first_name', label='First Name')
    second = django_filters.CharFilter(method='filter_second_name', label = 'Last Name')
    #ADD NETID TO FILTER

    class Meta:
        model = PHDMasterPOS
        fields = ()

    #Case Insensitive Filtering to check if search terms contain typed letters AND forms are Approved or Rejected by DGS
    def filter_first_name(self, queryset, name, value):
        return queryset.filter(Q(owner__first_name__icontains=value))

    def filter_second_name(self, queryset, name, value):
        return queryset.filter(Q(owner__last_name__icontains=value))
