from django.shortcuts import render
from TenantManagementApp.models import TblTenant
from TenantManagementApp.forms import TenantRegistratonForm,AgentForm


# Create your views here.
def index(request):
    return render(request,'TM_template/index.html',{'name':"Hanny"})

def addTenant(request):
    form=TenantRegistratonForm()
    if request.method=='POST':
        form=TenantRegistratonForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                tenant=form.save(commit=False)
                tenant.tn_agent = request.user
                tenant.tn_joining_date = request.POST.get('date_joined')
                tenant.save()
                return index(request)
            except Exception as e:
                print("Error:",e)
                print(form.errors)
        else:
            print(form.errors)

    return render(request,'TM_template/Agent/add_tenant.html',{'form':form})

def addAgent(request): 
    ag_form=AgentForm()
    if request.method=='POST':
        ag_form=AgentForm(request.POST,request.FILES)
        if ag_form.is_valid():
            try:
                agent=ag_form.save(commit=False)
                agent.date_joined = request.POST.get('date_joined')
                agent.set_password(agent.password)
                agent.normal_save()
                return index(request)
            except Exception as e:
                print("Error:",e)
                print(ag_form.errors)
        else:
            print(ag_form.errors)
    return render(request,'TM_template/AgentRegistration.html',{'ag_form':ag_form})