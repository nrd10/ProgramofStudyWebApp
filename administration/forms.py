from django.forms import ModelForm, ModelChoiceField, ModelMultipleChoiceField, IntegerField
from django.db.models import Q #allows for complex queries
from django.utils.html import escape
from shared.models import *
from django.conf import settings
import logging
from django_select2.forms import Select2Widget, Select2MultipleWidget, ModelSelect2MultipleWidget


class CourseForm(ModelForm):
    class Meta:
        model = Course
        exclude = ('id', )

    category = ModelMultipleChoiceField(label="Course Category", queryset=CourseType.objects.all(), widget=Select2MultipleWidget)
    concentration = ModelMultipleChoiceField(label="Concentration", queryset=Concentration.objects.all(), required=False, widget=Select2MultipleWidget)



class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser',
        'user_permissions', 'groups', 'is_staff', )

    advisor = ModelChoiceField(label="Advisor", queryset=User.objects.filter(user_type__icontains="Advisor"), required=False, widget=Select2Widget)
