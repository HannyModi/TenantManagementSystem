from django.contrib import admin
from TenantManagementApp.models import *

# Register your models here.
admin.site.register(Agent)
admin.site.register(Agent_allocation)
admin.site.register(Master_Property)
admin.site.register(Property)
admin.site.register(Property_Allocation)
admin.site.register(Property_Visit)
admin.site.register(Tenant)
admin.site.register(Rent_Collection)