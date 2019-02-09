from django.shortcuts import render,reverse
from TenantManagementApp.models import *
from TenantManagementApp.forms import TenantRegistratonForm, AgentForm
from django.contrib.auth import authenticate, login, logout
from TenantManagementApp.decorators import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def index(request):
    if request.method=='GET':
        if request.user.is_authenticated:
            logout(request)
    return render(request, 'TM_template/index.html')


def addTenant(request):
    form = TenantRegistratonForm()
    if request.method == 'POST':
        form = TenantRegistratonForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                tenant = form.save(commit=False)
                tenant.tn_agent = request.user
                tenant.tn_joining_date = request.POST.get('date_joined')
                tenant.save()
                return index(request)
            except Exception as e:
                print("Error:", e)
                print(form.errors)
        else:
            print(form.errors)

    return render(request, 'TM_template/Agent/add_tenant.html', {'form': form})


def addAgent(request):
    ag_form = AgentForm()
    if request.method == 'POST':
        ag_form = AgentForm(request.POST, request.FILES)
        if ag_form.is_valid():
            try:
                agent = ag_form.save(commit=False)
                agent.date_joined = request.POST.get('date_joined')
                agent.set_password(agent.password)
                agent.normal_save()
                return index(request)
            except Exception as e:
                print("Error:", e)
                print(ag_form.errors)
        else:
            print(ag_form.errors)
    return render(request, 'TM_template/AgentRegistration.html', {'ag_form': ag_form})


# custom login for admin/agent
def do_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user:
        if user.is_superuser:
            print("\n\n\n\n Admin \n", user, "\n\n\n")
            login(request, user)
            return render(request, 'TM_template/Admin/home.html')
        elif user.is_staff:
            print("\n\n\n\n Agent \n", user, "\n\n\n")
            login(request, user)
            return render(request, 'TM_template/Agent/Base.html')
        else:
            print("\n\n\n\nInavlid user\n\n\n\n")
            return render(request, 'TM_template/Index.html')
    else:
        print("\n\n\n\nInavlid user\n\n\n\n")
        return render(request, 'TM_template/Index.html')


# view all agent requests on admin site
# @login_required
@for_admin
def view_agent_request(request):
    try:
        agents = TblAgent.objects.filter(is_active=False, is_staff=False)
        page = request.GET.get('page', 1)
        paginator = Paginator(agents, 2)
        agents = paginator.page(page)
    except Exception as e:
        agents = None
        print('----> Error :', e)
    if agents:
        for agent in agents:
            print(agent)
    return render(request, 'TM_template/Admin/agent_requests.html', {'agents': agents})


# accepting the agent request
# @login_required
@for_admin
def agent_request_accept(request):
    id = request.POST['id']
    agent = TblAgent.objects.get(id=id)
    agent.verified_save()
    print("\n\n\n\n\n", agent)
    return view_agent_request(request)

# deleting the agent request
@for_admin
# @login_required
def agent_request_reject(request):
    id = request.POST['aid']
    agent = TblAgent.objects.filter(id=id).delete()
    # agent.verified_save()
    print("\n\n\n\n\n", agent)
    return view_agent_request(request)


# Viewing the agent request in more detailed View

@for_admin
def agent_profile(request):
    id = request.POST['aid']
    agent = TblAgent.objects.get(id=id)
    # agent.verified_save()
    # print("\n\n\n\n\n", agent)
    return render(request, 'TM_template/Admin/agent_profile.html', {'agent': agent})


def add_master_property(request):
    
    if request.method == "POST":
        msp_name=request.POST['mname']
        msp_address=request.POST['maddress']
        msp_description=request.POST['mdescription']
        msp_is_allocated = False
        msp_is_active = True
        try:
            mp= TblMasterProperty.objects.create(msp_name=msp_name,msp_address=msp_address,msp_description=msp_description,msp_is_allocated=msp_is_allocated,msp_is_active=msp_is_active)            
            mp.save()
            return adminhome(request)
        except Exception as e:
            print("Error :",e)
    else:
        return render(request,'TM_template/Admin/add_master_property.html')


def adminhome(request):
    return render(request,'TM_template/Admin/home.html')

def agenthome(request):
    return render(request,'TM_template/Agent/ag_home.html')


def add_property(request):
    address_list=[]
    if request.method == "POST":
        pr_master = TblMasterProperty.objects.get(id=request.POST['msp'])
        pr_address = request.POST['paddress']
        pr_rent = request.POST['prent']
        pr_deposite = request.POST['pdeposite']
        pr_is_allocated = False
        pr_is_active = True
        try:
            obj = TblProperty.objects.create(pr_master=pr_master,pr_address=pr_address,pr_rent=pr_rent,pr_deposite=pr_deposite,pr_is_active=pr_is_active,pr_is_allocated=pr_is_allocated)
            obj.save()
            return adminhome(request)
        except Exception as e:
            print("Error:",e)
    else:
        address_list=TblMasterProperty.objects.all()
    return render(request,'TM_template/Admin/add_property.html',{'address_list':address_list})

@for_admin
def view_approved_agent(request):
    try:
        agents = TblAgent.objects.filter(is_active=True, is_staff=True, is_superuser=False)
        page = request.GET.get('page', 1)
        paginator = Paginator(agents, 2)
        agents = paginator.page(page)
    except PageNotAnInteger:
        agents = paginator.page(1)
    except EmptyPage:
        agents = paginator.page(paginator.num_pages)
    except Exception as e:
        agents = None
        print('----> Error :', e)
    # if agents:
    #     for agent in agents:
    #         print(agent)
    return render(request, 'TM_template/Admin/all_approved_agents.html', {'agents': agents})


def agent_request_retire(request):
    id = request.POST['aid']
    agent = TblAgent.objects.filter(id=id)
    for obj in agent:
        obj.retire_agent()
    return HttpResponseRedirect(reverse(view_approved_agent))

def master_property_view(request):
    try:
        master_property_list=TblMasterProperty.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(master_property_list, 2)
        master_property_list = paginator.page(page)
    except PageNotAnInteger:
        master_property_list = paginator.page(1)
    except EmptyPage:
        master_property_list = paginator.page(paginator.num_pages)
    except Exception as e:
        master_property_list = None
        print('----> Error :', e)
    master_property_list=TblMasterProperty.objects.all()
    return render(request,'TM_template/Admin/master_property_view.html',{'master_property_list':master_property_list})

def allocate_msp(request,msp_id=None):
    obj_msp=TblMasterProperty.objects.get(id=msp_id)
    obj_agent=[]
    agent=""
    mp=""
    if request.method=='POST':
        al_master=TblMasterProperty.objects.get(id=request.POST['msp'])
        al_agent=TblAgent.objects.get(id=request.POST['agentx'])        
        obj=TblAgentAllocation.objects.get_or_create(al_agent=al_agent,al_master=al_master)
        print(obj[1])
        obj[0].save()
        return HttpResponseRedirect(reverse(adminhome))

    obj_agent=TblAgent.objects.filter(is_active=True, is_staff=True,is_superuser=False)
    return render(request,'TM_template/Admin/allocate_m_roperty.html',{'obj_msp':obj_msp,'obj_agent':obj_agent})