from django.core.exceptions import PermissionDenied
from TenantManagementApp.models import TblAgent
from django.shortcuts import render


def for_admin(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
           print("User is admin ")
           return function(request, *args, **kwargs)
        else:
            print("\n\n\n\nInavlid user\n\n\n\n")
            return render(request,'TM_template/Index.html') 
    return wrap

def for_staff(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
           print("User is admin ")
           return function(request, *args, **kwargs)
        else:
            print("\n\n\n\nInavlid user\n\n\n\n")
            return render(request,'TM_template/Base.html') 
    return wrap