from django.urls import path,re_path
from TenantManagementApp import views

urlpatterns = [
    path('',views.index, name='index'),
    re_path('AddTenant/',views.addTenant,name='addTenant'),
    path('AgentHome/',views.agenthome,name='agenthome'),
    path('ViewTenants/',views.view_tenants,name='view_tenants'),
    path('tenant_search_list/',views.tenant_search_result,name='tenant_search_result'),
    path('Agent_Properties/',views.allocated_property_list,name='allocated_property_view'),
    path('Tenant_Profile_view/',views.TenantDetails,name='TenantDetails'),
    path('Change_tenant_status/',views.change_tenant_status,name='change_tenant_status'),
    path('get_Tenant_list/',views.get_Tenant_list,name='get_Tenant_list'),
    path('allocate_property/',views.allocate_property,name='allocate_property'),
    path('deallocate_property/',views.deallocate_property,name='deallocate_property'),
    path('add_visit/',views.add_visit,name='add_visit'),
]