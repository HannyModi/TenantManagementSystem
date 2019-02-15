import datetime
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from TenantManagementApp.models import *
from TenantManagementApp.forms import *
from django.contrib.auth import authenticate, login, logout
from TenantManagementApp.decorators import *
from django.http import HttpResponseRedirect, HttpResponse

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
                agent.agent_save()
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
            return render(request, 'TM_template/Agent/Ag_home.html')
        else:
            print("\n\n\n\nInavlid user\n\n\n\n")
            return render(request, 'TM_template/Index.html')
    else:
        print("\n\n\n\nInavlid user\n\n\n\n")
        return render(request, 'TM_template/Index.html')


# view all agent requests on admin site
@for_admin
def view_agent_request(request):
    try:
        agents = TblAgent.objects.filter(is_active=False, is_staff=False)
    except Exception as e:
        agents = None
        print('----> Error :', e)
    if agents:
        for agent in agents:
            print(agent)
    return render(request, 'TM_template/Admin/agent_requests.html', {'agents': agents})

# accepting the agent request
@for_admin
def agent_request_accept(request):
    id = request.POST['id']
    agent = TblAgent.objects.get(id=id)
    agent.verified_save()
    print("\n\n\n\n\n", agent)
    return view_agent_request(request)

# deleting the agent request
@for_admin
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

@for_admin
def add_master_property(request):   
    if request.method == "POST":
        lst = request.POST
        for l in lst.keys():
            print(l,"   ",lst[l])

    if request.method == "POST":

        try:
            # Creating new or taking Existing object for master property.
            msp = TblMasterProperty.objects.get_or_create(msp_name=request.POST['msp_name'],
                                                          msp_address=request.POST['msp_address'],
                                                          msp_description=request.POST['msp_description'],
                                                          msp_is_active=True)
            # Condition to check if new row is created or not.
            if msp[1]:
                # Saving the object and creating master clone if new row created.
                msp[0].new_save()
                no = int(request.POST['msp_clone_no'])
                if request.POST['msp_have_clones'] and no > 0 and no <= 5:
                    for n in range(1, no+1):
                        cln = TblMasterPropertyClone.objects.create(
                            cln_alias=request.POST['msp_clone'+str(n)],
                            cln_master=msp[0],cln_is_allocated=False,cln_is_active=True)
                        cln.save()
                return adminhome(request)
            else:
                return render(request, 'TM_template/Admin/add_master_property.html',
                              {'context': 'Master Property already exists'})

        except Exception as e:
            print("Error :", e)
    else:
        return render(request,'TM_template/Admin/add_master_property.html')

def adminhome(request):
    return render(request,'TM_template/Admin/home.html')

def agenthome(request):
    return render(request,'TM_template/Agent/ag_home.html')

def add_property(request):
    address_list = TblMasterProperty.objects.all()
    existing_addresses = []
    addeed_addresses = []
    if request.method == "POST":
        # A function to check if property alredy exists
        def is_property_exists(msp=None, add=None):
            is_exists = False
            clones = TblMasterPropertyClone.objects.filter(cln_master=msp)
            for clone in clones:
                if TblProperty.objects.filter(pr_master=clone, pr_address=add).exists():
                    is_exists = True
                    break
            return is_exists

        msp_id = request.POST['pr_msp']
        msp_clone_id = request.POST['pr_msp_clone']
        num = request.POST['pr_num']
        pr_rent = request.POST['pr_rent']
        pr_deposite = request.POST['pr_deposite']
        pr_description = request.POST['pr_description']
        msp = TblMasterProperty.objects.get(id=msp_id)
        msp_clone = TblMasterPropertyClone.objects.get(id=msp_clone_id)
        for n in range(int(num)):
            if 'pr_address'+str(n) in request.POST.keys():
                pr_address = request.POST['pr_address'+str(n)]
                if not is_property_exists(msp=msp, add=pr_address):
                    try:
                        obj = TblProperty.objects.create(pr_master=msp_clone,
                                                         pr_address=pr_address,
                                                         pr_rent=pr_rent,
                                                         pr_deposite=pr_deposite,
                                                         pr_description=pr_description,
                                                         pr_is_active=True,
                                                         pr_is_allocated=False)
                        obj.save()
                        addeed_addresses.append(pr_address)
                    except Exception as e:
                        print("\n\n\n\nError:", e)
                else:
                    existing_addresses.append(pr_address)
        if existing_addresses:
            context = ",".join(existing_addresses)+" are alredy existing in <b><u>" + \
                msp.msp_name+"</u></b> Master Property.."
        else:
            context = None
        if addeed_addresses:
            success = ",".join(addeed_addresses)+" are added in <b><u>"+msp_clone.cln_alias + \
                "</b></u> clone of <b><u>"+msp.msp_name+"<b></u> Master Property."
        else:
            success = "No Property added to <b><u>"+msp_clone.cln_alias + \
                "</u></b> clone of <b><u>"+msp.msp_name+"</u></b> Master Property."
        return render(request, 'TM_template/Admin/add_property.html', {'address_list': address_list, 'context': context, 'success': success})

    return render(request,'TM_template/Admin/add_property.html',{'address_list':address_list})

@for_admin
def view_approved_agent(request):
    try:
        agents = TblAgent.objects.filter(is_active=True, is_staff=True, is_superuser=False).order_by('first_name', 'last_name')
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
    except Exception as e:
        master_property_list = None
        print('----> Error :', e)
    master_property_list=TblMasterProperty.objects.all()
    allocated_mp=TblAgentAllocation.objects.all()
    return render(request,'TM_template/Admin/master_property_view.html',{'master_property_list':master_property_list,'allocated_mp':allocated_mp})

def allocate_msp(request,msp_id=None):
    obj_msp=TblMasterProperty.objects.get(id=msp_id)
    obj_agent=[]
    if request.method=='POST':
        al_master=TblMasterProperty.objects.get(id=request.POST['msp'])
        al_agent=TblAgent.objects.get(id=request.POST['agentx'])        
        obj=TblAgentAllocation.objects.get_or_create(al_agent=al_agent,al_master=al_master)
        print(obj[1])
        obj[0].save()
        return HttpResponseRedirect(reverse(adminhome))

    obj_agent=TblAgent.objects.filter(is_active=True, is_staff=True,is_superuser=False)
    return render(request,'TM_template/Admin/allocate_m_roperty.html',{'obj_msp':obj_msp,'obj_agent':obj_agent})

def master_property_soldout(request,msp_id):
    obj_msp=TblMasterProperty.objects.get(id=msp_id)
    try:
        obj_msp.msp_is_active=False
        obj_msp.save()
        
    except Exception as e:
        print("Error: ",e)
    return HttpResponseRedirect(reverse(master_property_view))

def property_listview(request):
    try:
        property_list=TblProperty.objects.all()

    except Exception as e:
        property_list = None
        print('----> Error :', e)
    property_list=TblProperty.objects.all()
    mp_list=TblMasterProperty.objects.all()
    return render(request,'TM_template/Admin/property_view.html',{'property_list':property_list,'mp_list':mp_list})

def property_soldout(request,pr_id):
    obj_pr=TblProperty.objects.get(id=pr_id)
    try:
        obj_pr.pr_is_active=False
        obj_pr.save()        
    except Exception as e:
        print("Error: ",e)
    return HttpResponseRedirect(reverse(property_listview))

def contactus(request):
    return render(request,'TM_template/contact.html')

def view_tenants(request):
    tenantlist=TblTenant.objects.filter(tn_agent_id=request.user.id)
    return render(request,'TM_template/Agent/view_tenant.html',{'tenantlist':tenantlist})

# Creating Clone Input boxes according to user input
@for_admin
def clone_list(request):
    clones = TblMasterPropertyClone.objects.filter(cln_master=request.GET['msp']).order_by('id')
    return render(request, 'TM_template/Admin/clone_list.html', {'clones': clones})

# returning search result of agent requests.
def get_agents(starts_with=''):
    agents = []
    if starts_with:
        agents = TblAgent.objects.filter(first_name__istartswith=starts_with,
                                         is_active=False,
                                         is_staff=False).order_by('first_name',
                                                                  'last_name')
        print(agents)
    else:
        agents = TblAgent.objects.filter(is_active=False,
                                         is_staff=False).order_by('first_name',
                                                                  'last_name')
    return agents


# View the search result from agent requests
@for_admin
def agent_requests_search(request):
    agents = []
    starts_with = ''
    if request.method == 'GET':
        if 'suggestion' in request.GET.keys():
            starts_with = request.GET['suggestion']
        agents = get_agents(starts_with)
        print("ajax",agents)
    return render(request, 'TM_template/Admin/s_agents.html', {'agents': agents})

# Creating Clone Input boxes according to user input
def create_clone_list(request):
    no = request.GET['clone_no']
    if no == '':
        no = 0
    return render(request, 'TM_template/Admin/clone_input_list.html', {'no': range(1, int(no)+1)})
