from django.urls import path,re_path
from TenantManagementApp import views

urlpatterns = [
    path('all_approved_agents',views.view_approved_agent, name='view_approved_agent'),
    path('agent_requests/',views.view_agent_request, name="agent_requests"),
    path('agent_request_accept/',views.agent_request_accept, name='agent_request_accept'),
    path('agent_request_reject/',views.agent_request_reject, name='agent_request_reject'),
    path('agent_request_retire/',views.agent_request_retire, name='agent_request_retire'),
    path('view_master_property/',views.master_property_view,name='master_property_view'),
    path('allocate_master_property/',views.allocate_msp,name='allocate_msp'),
    # path('(P?<msp_id>[\w\-]+)/allocate_master_property/',views.allocate_msp,name='allocate_msp'),
    path('(P?<msp_id>[\w\-]+)/master_property_soldout/',views.master_property_soldout,name='master_property_soldout'),
    path('(P?<pr_id>[\w\-]+)/property_soldout/',views.property_soldout,name='property_soldout'), 
    path('properties/',views.property_listview,name='property_listview'),   
    path('agent_profile/',views.agent_profile, name='agent_profile'),
    path('add/property/',views.add_property,name='add_property'),
    path('add_master_property/',views.add_master_property, name='add_master_property'),
    path('home/',views.adminhome,name='adminhome'),
    path('master_clone_list/',views.create_clone_list,name='admin_create_clone_list'),
    path('property_clone_list/',views.clone_list,name='admin_show_clone_list'),
    path('agent_request_search/',views.agent_requests_search, name='agent_requests_search'),
    path('active_agent_search/',views.active_agent_search, name='active_agent_search'),


]