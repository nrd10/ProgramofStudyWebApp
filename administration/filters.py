from shared.models import *
import django_filters
from django_filters.widgets import LinkWidget
from django_select2.forms import *
from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField
from django.db.models import Q #allows for complex queries
from django_filters import *


POSTYPE_MULTI = []
POSTYPE_MULTI.append((1, "MEng"))
POSTYPE_MULTI.append((2, "MS"))
POSTYPE_MULTI.append((3, "PhD"))
POSTYPE_MULTI.append((4, "Advisor"))
POSTYPE_MULTI.append((5, "DGS"))
POSTYPE_MULTI.append((6, "Administrator"))


class CourseFilter(django_filters.FilterSet):
    # '''filter for MengPOS items'''
    custom_listing = django_filters.CharFilter(method='filter_listing_name', label='Listing')
    custom_title = django_filters.CharFilter(method='filter_title_name', label = 'Title')
    #ADD NETID TO FILTER

    class Meta:
        model = Course
        fields = ('custom_listing', 'custom_title', 'category', 'concentration',)

    #Case Insensitive Filtering to check if search terms contain typed letters
    def filter_listing_name(self, queryset, name, value):
        return queryset.filter(Q(listing__icontains=value))

    def filter_title_name(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value))


class UserFilter(django_filters.FilterSet):
    # '''filter for MengPOS items'''
    custom_netid = django_filters.CharFilter(method='filter_netid', label='NetID')
    custom_email = django_filters.CharFilter(method='filter_email', label = 'Email')
    custom_first_name = django_filters.CharFilter(method='filter_first_name', label='First Name')
    custom_last_name = django_filters.CharFilter(method='filter_last_name', label = 'Last Name')
    # custom_user_type = django_filters.MultipleChoiceFilter(choices=POSTYPE_MULTI)
    #ADD NETID TO FILTER

    class Meta:
        model = User
        fields = ('custom_netid', 'custom_email', 'custom_first_name',
        'custom_last_name',)

    #Case Insensitive Filtering to check if search terms contain typed letters
    def filter_netid(self, queryset, name, value):
        return queryset.filter(Q(netid__icontains=value))

    def filter_email(self, queryset, name, value):
        return queryset.filter(Q(email__icontains=value))

    def filter_first_name(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value))

    def filter_last_name(self, queryset, name, value):
        return queryset.filter(Q(last_name=value))
