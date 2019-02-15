from django.urls import path,re_path
from TenantManagementApp import views

urlpatterns = [
    path('',views.index, name='index'),
    re_path('^AddTenant/$',views.addTenant,name='addTenant'),
    path('AgentHome/',views.agenthome,name='agenthome'),
    path('ViewTenants/',views.view_tenants,name='view_tenants'),

]