from django.urls import path,re_path
from TenantManagementApp import views

urlpatterns = [
    path('',views.index, name='index'),
]