from django.contrib import admin
from meng.models import *
from meng.forms import MEngPOSForm
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin


# Register your models here.
admin.site.register(MEngComment)
@admin.register(MEngPOS)
class MengPOSAdmin(AjaxSelectAdmin):
    list_display = ('id', 'owner')
    form = MEngPOSForm
