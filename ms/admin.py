from django.contrib import admin
from ms.models import *
from ms.forms import *
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

# Register your models here.
admin.site.register(MSCourseComment)
admin.site.register(MSProjectComment)
admin.site.register(MSThesisComment)

@admin.register(MSCoursePOS)
class MscoursePOSAdmin(AjaxSelectAdmin):
    list_display = ('id', 'owner')
    form = MSCoursePOSForm

@admin.register(MSProjectPOS)
class MsprojectPOSAdmin(AjaxSelectAdmin):
    list_display = ('id', 'owner')
    form = MSProjectPOSForm

@admin.register(MSThesisPOS)
class MsthesisPOSAdmin(AjaxSelectAdmin):
    list_display = ('id', 'owner')
    form = MSThesisPOSForm
