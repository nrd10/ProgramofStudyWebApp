from django.contrib import admin
from phd.models import *
from phd.forms import *
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin

admin.site.register(CurricularArea)
admin.site.register(PHDBachelorComment)
admin.site.register(PHDMasterComment)

# Register your models here.
@admin.register(PHDBachelorPOS)
class PhdbachelorPOSAdmin(AjaxSelectAdmin):
    list_display = ('id', 'owner')
    form = PHDBSPOSForm

@admin.register(PHDMasterPOS)
class PhdmasterPOSAdmin(AjaxSelectAdmin):
    list_display = ('id', 'owner')
    form = PHDMSPOSForm
