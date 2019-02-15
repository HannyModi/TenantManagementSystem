"""TenantManagementProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from TenantManagementApp import adminurl,views,agenturls
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    re_path('^$',views.index, name='index'),
    path('login/',views.do_login, name= 'login'),
    path('contact us/',views.contactus,name='contactus'),
    # path('forgot_password/',views.forgotpwd,name='forgotpwd'),
    re_path('^AgentRegistration/$',views.addAgent, name='addAgent'), 
    path('pwd_reset/',include('password_reset.urls')),  
    # path('pwd_reset/',include(('password_reset.urls', 'pwd_reset'), namespace='pwd_reset')),
    path('Agent/',include(agenturls)),
    path('Admin/',include(adminurl)),
    path('admin/', admin.site.urls),
    
   
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
