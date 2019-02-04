from django.contrib import admin
from TenantManagementApp.models import *
# Register your models here.

admin.site.register(TblAgent)
admin.site.register(TblAgentAllocation)
admin.site.register(TblMasterProperty)
admin.site.register(TblProperty)
admin.site.register(TblPropertyAllocation)
admin.site.register(TblRentAllocation)
admin.site.register(TblTenant)
admin.site.register(TblVisit)