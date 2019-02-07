from django.contrib import admin
from django.contrib import auth
from TenantManagementApp.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from TenantManagementApp.forms import *
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# Register your models here.
class AgentAdmin(UserAdmin):
    add_form = AgentCreationForm
    form = AgentChangeForm
    model = TblAgent
    list_display = ['email', 'username',]


admin.site.register(TblAgent, AgentAdmin)


admin.site.register(TblAgentAllocation)
admin.site.register(TblMasterProperty)
admin.site.register(TblProperty)
admin.site.register(TblPropertyAllocation)
admin.site.register(TblRentAllocation)
admin.site.register(TblTenant)
admin.site.register(TblVisit)