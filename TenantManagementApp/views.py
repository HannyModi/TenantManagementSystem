import datetime
from django.conf import settings
from django.shortcuts import render
from django.urls import reverse
from TenantManagementApp.models import *
from TenantManagementApp.forms import *
from django.contrib.auth import authenticate, login, logout
from TenantManagementApp.decorators import *
from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction
# Create your views here.
# redirects to index page


def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
    return render(request, 'TM_template/index.html')

# Agent sends request to admin for his account in this wesite


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
            # print("\n\n\n\n Admin \n", user, "\n\n\n")
            login(request, user)
            return HttpResponseRedirect(reverse(adminhome))
        elif user.is_staff:
            # print("\n\n\n\n Agent \n", user, "\n\n\n")
            login(request, user)
            return HttpResponseRedirect(reverse(agenthome))
        else:
            # print("\n\n\n\nInavlid user\n\n\n\n")
            return HttpResponseRedirect(reverse(index))
    else:
        # print("\n\n\n\nInavlid user\n\n\n\n")
        return render(request, 'TM_template/Index.html')


# view all agent requests on admin site
@for_admin
def view_agent_request(request):
    try:
        agents = TblAgent.objects.filter(is_active=False, is_staff=False)
    except Exception as e:
        agents = None
        print('----> Error :', e)
    # if agents:
    #     for agent in agents:
    #         # print(agent)
    return render(request, 'TM_template/Admin/agent_requests.html', {'agents': agents})

# accepting the agent request


@for_admin
def agent_request_accept(request):
    id = request.POST['id']
    agent = TblAgent.objects.get(id=id)
    agent.verified_save()
    # print("\n\n\n\n\n", agent)
    return view_agent_request(request)

# deleting the agent request


@for_admin
def agent_request_reject(request):
    id = request.POST['aid']
    agent = TblAgent.objects.filter(id=id).delete()
    # agent.verified_save()
    # print("\n\n\n\n\n", agent)
    return view_agent_request(request)

# Viewing the agent request in more detailed View


@for_admin
def agent_profile(request):
    id = request.POST['aid']
    agent = TblAgent.objects.get(id=id)
    # agent.verified_save()
    # # print("\n\n\n\n\n", agent)
    return render(request, 'TM_template/Admin/agent_profile.html', {'agent': agent})

# Adding a new master property


@for_admin
def add_master_property(request):
    # if request.method == "POST":
    #     lst = request.POST
    #     for l in lst.keys():
    #         # print(l, "   ", lst[l])

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
                if request.POST['msp_have_clones'] and no > 0 and no <= 50:
                    for n in range(1, no+1):
                        cln = TblMasterPropertyClone.objects.create(
                            cln_alias=request.POST['msp_clone'+str(n)],
                            cln_master=msp[0], cln_is_allocated=False, cln_is_active=True)
                        cln.save()
                return adminhome(request)
            else:
                return render(request, 'TM_template/Admin/add_master_property.html',
                              {'context': 'Master Property already exists'})

        except Exception as e:
            print("Error :", e)
    else:
        return render(request, 'TM_template/Admin/add_master_property.html')

# redirect to admin home


@for_admin
def adminhome(request):
    return render(request, 'TM_template/Admin/home.html')

# To Add Property


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

    return render(request, 'TM_template/Admin/add_property.html', {'address_list': address_list})

# Editing Property details


@for_admin
def edit_property(request):
    try:
        pr = TblProperty.objects.get(id=request.GET.get('id'))
        pr.pr_rent = request.GET.get('rent')
        pr.pr_deposite = request.GET.get('deposite')
        pr.pr_description = request.GET.get('description')
        pr.save()
        return HttpResponse("1")
    except Exception as e:
        # print("error ", e)
        return HttpResponse("0")

# showing data on admin page


@for_admin
def show_data(request):

    try:
        act = request.GET.get('act')
        id = request.GET.get('id')
        # print(act)
        data = None
        if act == 'all_clones':
            data = TblMasterPropertyClone.objects.filter(
                cln_master=id).order_by('-cln_is_master_clone', 'cln_alias')

            # for d in data:
            #     # print(d.cln_alias)
        elif act == 'allocated_clones':
            data = TblAgentAllocation.objects.select_related(
                'al_agent').select_related('al_master'
                                           ).filter(al_master__cln_master=id,
                                                    al_master__cln_is_allocated=True
                                                    ).order_by(
                '-al_master__cln_is_master_clone',
                'al_master__cln_alias')

            # for d in data:
            #     # print(d.al_agent.username, d.al_master.cln_alias)
        elif act == 'unallocated_clones':
            data = TblMasterPropertyClone.objects.filter(cln_master=id,
                                                         cln_is_allocated=False
                                                         ).order_by(
                '-cln_is_master_clone', 'cln_alias')

            # for d in data:
                # print(d.cln_alias)
        elif act == 'all_properties':
            data = TblProperty.objects.select_related('pr_master'
                                                      ).filter(pr_master__cln_master=id).order_by(
                '-pr_master__cln_is_master_clone',
                'pr_master__cln_alias',
                'pr_address')

            # for d in data:
                # print(d.pr_master.cln_alias, d.pr_address)
        elif act == 'allocated_properties':

            data = TblPropertyAllocation.objects.select_related(
                'pa_tenant').select_related(
                    'pa_property').filter(
                        pa_property__pr_master__cln_master=id
            ).order_by(
                '-pa_property__pr_master__cln_is_master_clone',
                'pa_property__pr_master__cln_alias',
                'pa_property__pr_address')
            # for d in data:
                # print(d.pa_property.pr_master.cln_alias,
                    #   d.pa_property.pr_address, d.pa_tenant.tn_name)
            data = TblAgentAllocation.objects.select_related(
                'al_agent').select_related('al_master'
                                           ).filter(al_master__cln_master=id)
        elif act == 'unallocated_properties':
            data = TblProperty.objects.select_related('pr_master'
                                                      ).filter(pr_master__cln_master=id,
                                                               pr_is_allocated=False
                                                               ).order_by(
                '-pr_master__cln_is_master_clone',
                'pr_master__cln_alias',
                'pr_address')

            # for d in data:
                # print(d.pr_master.cln_alias, d.pr_address)
        # data= TblMasterPropertyClone.objects.prefetch_related(Prefetch(

        # ))
        # data = TblAgentAllocation.objects.select_related('al_agent').prefetch_related(Prefetch('al_master',
        #       queryset=TblMasterPropertyClone.objects.filter(cln_master=id,cln_is_allocated=True),
        #       to_attr='master'))
        # data = TblAgentAllocation.objects.select_related(
        #     'al_agent').select_related('al_master'
        #                                ).filter(al_master__cln_master=id)

        # .prefetch_related(Prefetch('al_master',
        #   queryset=TblMasterPropertyClone.objects.filter(cln_master=id
        #   ))).all()
        # print(data)

        return render(request, 'TM_template/Admin/show_data.html', {'rows': data, 'act': act, 'msp': id})
    except Exception as e:
        print("error ", e)
        return HttpResponse('<div  style="color: red; align: right; width: max-content; " ><right>Something Went Wrong While Fetching Requested data</right></div>')

# Deallocating property


@for_admin
def deallocate_clone(request):
    try:
        al = TblAgentAllocation.objects.get(id=request.GET.get('id'))
        al.al_master.cln_is_allocated = False
        al.al_master.save()
        al.delete()
        return HttpResponse("1")
    except Exception as e:
        print("error ", e)
        return HttpResponse("0")


# Deleting Master property
def delete_master_property(request):
    try:
        msp = TblMasterProperty.objects.get(id=request.GET.get('id'))
        tenants = TblPropertyAllocation.objects.select_related('pa_tenant').select_related(
            'pa_property').select_related('pa_property__pr_master').filter(pa_property__pr_master__cln_master=msp)
        for tenant in tenants:
            tenant.pa_tenant.tn_status = 0
            tenant.pa_tenant.save()
            # print(tenant.pa_tenant)
            # tenant.pa_is_allocated = False
            # tenant.save()
        msp.delete()
        return HttpResponse("1")
    except Exception as e:
        # print('Error at Master property delete', e)
        return HttpResponse("0")


@for_admin
def view_approved_agent(request):
    try:
        agents = TblAgent.objects.filter(
            is_staff=True, is_superuser=False).order_by('first_name', 'last_name')
    except Exception as e:
        agents = None
        # print('----> Error :', e)
    # if agents:
    #     for agent in agents:
    #         # print(agent)
    return render(request, 'TM_template/Admin/all_approved_agents.html', {'agents': agents})


def agent_request_retire(request):
    agent = TblAgent.objects.get(id=request.GET['id'])
    act = request.GET['is_active']
    if act == '0':
        # print('dealloacting all properties')
        try:
            allocation = TblAgentAllocation.objects.select_related(
                'al_master').filter(al_agent=request.GET['id'])
            # print(allocation)
            for al in allocation:
                # print(al.al_master.cln_alias)
                al.al_master.cln_is_allocated = False
                al.al_master.save()
            allocation.delete()
        except Exception as e:
            print('Error at deallocation', e)
    agent.is_active = act
    agent.save()
    return HttpResponseRedirect(reverse(view_approved_agent))


def master_property_view(request):
    master_property_list = ViewMasterProperties.objects.all()
    return render(request, 'TM_template/Admin/master_property_view.html', {'master_property_list': master_property_list})

# Allocating Agent


@for_admin
def allocate_msp(request):

    if request.method == 'GET':
        obj_msp = TblMasterProperty.objects.all()
        obj_agent = TblAgent.objects.filter(
            is_active=True, is_staff=True, is_superuser=False)
        if 'msp' in request.GET.keys() and 'cln' in request.GET.keys():
            msp = TblMasterProperty.objects.get(id=request.GET['msp'])
            cln = TblMasterPropertyClone.objects.get(id=request.GET['cln'])
            return render(request, 'TM_template/Admin/allocate_m_roperty.html',
                          {'obj_msp': obj_msp,
                           'obj_agent': obj_agent,
                           'msp': msp,
                           'cln': cln,
                           'agent': None})
        elif 'agent' in request.GET.keys():
            agent = TblAgent.objects.get(id=request.GET.get('agent'))
            return render(request, 'TM_template/Admin/allocate_m_roperty.html',
                          {'obj_msp': obj_msp,
                           'obj_agent': obj_agent,
                           'msp': None,
                           'cln': None,
                           'agent': agent})
        else:
            return render(request, 'TM_template/Admin/allocate_m_roperty.html',
                          {'obj_msp': obj_msp,
                           'obj_agent': obj_agent,
                           'msp': None,
                           'cln': None,
                           'agent': None})

    elif request.method == 'POST':
        try:
            # print("Hi")
            # print("Clone id", request.POST['pr_msp_clone'])
            # al_master=TblMasterProperty.objects.get(id=request.POST['pr_msp'])
            al_master = TblMasterPropertyClone.objects.get(
                id=request.POST['pr_msp_clone'])
            al_master.cln_is_allocated = True
            al_master.save()
            al_agent = TblAgent.objects.get(id=request.POST['agentx'])
            obj = TblAgentAllocation.objects.get_or_create(
                al_agent=al_agent, al_master=al_master)
            # print(obj[1])
            obj[0].save()
            return HttpResponseRedirect(reverse(master_property_view))
        except Exception as e:
            # print('Error ', e)
            return HttpResponseRedirect(reverse(master_property_view))
    else:
        HttpResponse("Error")


def master_property_soldout(request, msp_id):
    obj_msp = TblMasterProperty.objects.get(id=msp_id)
    mpclone_list = TblMasterPropertyClone.objects.filter(cln_master_id=msp_id)
    # print(mpclone_list)
    try:
        obj_msp.msp_is_active = False
        obj_msp.save()

    except Exception as e:
        print("Error: ", e)
    return HttpResponseRedirect(reverse(master_property_view))


def property_listview(request):
    try:
        property_list = property_view.objects.all().order_by('pr_address', 'msp_address')
        # for p in property_list:
        #     # print(p.pr_address)
        # # .values('cln_alias')
        # # # print(property_list.count())
        # # # print(property_list)
    except Exception as e:
        property_list = None
        print('----> Error :', e)
    return render(request, 'TM_template/Admin/property_view.html', {'property_list': property_list, })


def property_soldout(request):
    obj_pr = TblProperty.objects.get(id=request.GET['pr_id'])
    try:
        obj_pr.pr_is_active = False
        obj_pr.pr_is_allocated = False
        obj_pr.save()
    except Exception as e:
        print("Error: ", e)
    return HttpResponse("1")


def contactus(request):
    return render(request, 'TM_template/contact.html')

# Creating Clone Input boxes according to user input


@for_admin
def clone_list(request):
    clones = TblMasterPropertyClone.objects.filter(
        cln_master=request.GET['msp']).order_by('id')
    return render(request, 'TM_template/Admin/clone_list.html', {'clones': clones})

# for Master Property allocation


@for_admin
def unallocated_clone_list(request):
    clones = TblMasterPropertyClone.objects.filter(
        cln_master=request.GET['msp'], cln_is_allocated=False).order_by('id')
    # print(clones)
    return render(request, 'TM_template/Admin/clone_list.html', {'clones': clones})


# returning search result of agent requests.
def get_agents(starts_with=''):
    agents = []
    first_name = starts_with
    last_name = None
    if ' ' in starts_with:
        list1 = starts_with.split(' ')
        first_name = list1[0]
        last_name = list1[1]

    if first_name:
        if last_name:

            agents = TblAgent.objects.filter(first_name__istartswith=first_name,
                                             last_name__istartswith=last_name,
                                             is_active=False,
                                             is_staff=False).order_by('first_name',
                                                                      'last_name')
        else:

            agents = TblAgent.objects.filter(first_name__istartswith=first_name,
                                             is_active=False,
                                             is_staff=False).order_by('first_name',
                                                                      'last_name')
        # print(agents)

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
        # print("ajax", agents)
    return render(request, 'TM_template/Admin/s_agents.html', {'agents': agents})

# Creating Clone Input boxes according to user input


def create_clone_list(request):
    no = request.GET['clone_no']
    if no == '':
        no = 0
    return render(request, 'TM_template/Admin/clone_input_list.html', {'no': range(1, int(no)+1)})

# returning search result of all agent.


def get_active_agents(starts_with=''):
    agents = []
    first_name = starts_with
    last_name = None
    if ' ' in starts_with:
        list1 = starts_with.split(' ')
        first_name = list1[0]
        last_name = list1[1]

    if first_name:
        if last_name:

            agents = TblAgent.objects.filter(first_name__istartswith=first_name,
                                             last_name__istartswith=last_name, is_superuser=False,
                                             is_staff=True).order_by('first_name',
                                                                     'last_name')
        else:

            agents = TblAgent.objects.filter(first_name__istartswith=first_name,
                                             is_superuser=False,
                                             is_staff=True).order_by('first_name',
                                                                     'last_name')
        # print(agents)

    else:
        agents = TblAgent.objects.filter(is_staff=True, is_superuser=False).order_by('first_name',
                                                                                     'last_name')
    return agents


# View the search result from all agent
@for_admin
def active_agent_search(request):
    agents = []
    starts_with = ''
    if request.method == 'GET':
        if 'suggestion' in request.GET.keys():
            starts_with = request.GET['suggestion']
        agents = get_active_agents(starts_with)
        # print("ajax", agents)
    return render(request, 'TM_template/Admin/agents.html', {'agents': agents})


'''Creating extra clones after master property is created.'''


@for_admin
def create_clone(request):
    msp_list = []
    if request.method == 'POST':
        obj_msp = TblMasterProperty.objects.get(id=request.POST['pr_msp'])
        no = int(request.POST['msp_clone_no'])
        if no > 0 and no <= 50:
            for n in range(1, no+1):
                cln = TblMasterPropertyClone.objects.create(
                    cln_alias=request.POST['msp_clone'+str(n)],
                    cln_master=obj_msp, cln_is_allocated=False, cln_is_active=True)
                cln.save()

    else:
        msp_list = TblMasterProperty.objects.all()

    return render(request, 'TM_Template/Admin/create_clone.html', {'obj_msp': msp_list})

# ------------------------------------------------
# Agent Methods
# ------------------------------------------------


@for_staff
def view_tenants(request):
    tenantlist = TblTenant.objects.filter(tn_agent_id=request.user.id)
    return render(request, 'TM_template/Agent/view_tenant.html', {'tenantlist': tenantlist})


@for_staff
def addTenant(request):
    form = TenantRegistratonForm()
    if request.method == 'POST':
        form = TenantRegistratonForm(request.POST, request.FILES)
        if form.is_valid():
            # print("\n\n\n Pass \n\n\n")
            try:
                tenant = form.save(commit=False)
                tenant.tn_agent = request.user
                tenant.tn_joining_date = request.POST.get('date_joined')
                tenant.tn_is_active = True
                tenant.save()
                print(tenant)
                plist = allocated_property_view.objects.filter(
                        agent_id=request.user, pr_is_active=True, pr_is_allocated=False)
                context={'tenant':tenant,'plist':plist}
                return render(request,'TM_template/Agent/add_visit.html',context)
    #             # return agenthome(request)
            except Exception as e:
                print("Error:", e)
                print(form.errors)
        else:
            print(form.errors)
            
    return render(request, 'TM_template/Agent/add_tenant.html', {'form': form})


'''List of properties allocated to a perticular agent by admin'''


@for_staff
def allocated_property_list(request):

    # allocated_pr=TblAgentAllocation.objects.filter(al_agent=request.user).select_related('al_agent').prefetch_related('al_master');
    allocated_pr = allocated_property_view.objects.filter(
        agent_id=request.user)
    # for obj in allocated_pr:
    #     # print(obj.al_master.cln_alias,obj.al_master.cln_alias.pr_name,obj.al_agent.username)
    return render(request, 'TM_template/Agent/agent_property.html', {'allocated_pr': allocated_pr})


'''Agent can see which properties are rented and which are not.'''


@for_staff
def rented_property_list(request):
    allocated_pr = allocated_property_view.objects.filter(
        agent_id=request.user)

    return render(request, 'TM_template/Agent/agent_property.html', {'allocated_pr': allocated_pr})


'''view tenant Details'''


@for_staff
def TenantDetails(request):
    if request.method == 'POST':
        try:
            tenant = TblTenant.objects.get(id=request.POST['tid'])
            # print(tenant)
            return render(request, 'TM_template/Agent/view_tenant_detail.html', {'tenant': tenant})
        except Exception as e:
            print(e)
    else:
        return view_tenants(request)

# redirect to agent home


@for_staff
def agenthome(request):
    return render(request, 'TM_template/Agent/ag_home.html')


'''To make tenant deactivate'''


@for_staff
def change_tenant_status(request):
    tenant = TblTenant.objects.get(id=request.POST['tid'])
    try:
        if tenant.tn_is_active == False:
            tenant.tn_is_active = True
        else:
            tenant.tn_is_active = False
        tenant.save()
    except Exception as e:
        print("\n\nErorr:----------->", e)
    return view_tenants(request)


def tenant_search_result(request):
    tenantlist = []
    starts_with = ''
    try:
        if request.method == 'GET':
            if 'suggestion' in request.GET.keys():
                user = request.user.id
                starts_with = request.GET['suggestion']
                tenantlist = tenant_search(user, starts_with)
            # print("\nTenant list:\n", tenantlist)
    except Exception as e:
        print(e)
    return render(request, 'TM_template/Agent/tenants.html', {'tenantlist': tenantlist})


def tenant_search(user, suggestion=None):
    tn_list = []
    if suggestion:
        tn_list = TblTenant.objects.filter(
            tn_name__istartswith=suggestion, tn_agent=user)
        # print("\n\n\n", tn_list)
    else:
        tn_list = TblTenant.objects.filter(tn_agent=user)
        # print("\n\n\n", tn_list)
    return tn_list


def get_Tenant_list(request):
    if 'pid' in request.GET.keys():
        pobj = allocated_property_view.objects.get(
            property_id=request.GET['pid'])
        # print(request.GET['pid'])
        # print(pobj.pr_address, pobj.msp_name, pobj.msp_address)
        Tenant_list = TblTenant.objects.filter(
            tn_is_active=True, tn_agent_id=request.user, tn_status=1)
        # print(Tenant_list)
        context = {'pobj': pobj,
                   'Tenant_list': Tenant_list, 'page': "pdetails"}
    elif 'tid' in request.GET.keys():
        ten = TblTenant.objects.get(id=request.GET['tid'], tn_is_active=True)
        # Add filter for already allocated properties to the tenants tooo
        plist = allocated_property_view.objects.filter(
            agent_id=request.user, pr_is_active=True, pr_is_allocated=False)
        # for p in plist:
            # print(p.msp_name)
        context = {'ten': ten, 'plist': plist, 'page': "tdetails"}
    else:
        Tenant_list = TblTenant.objects.filter(
            tn_is_active=True, tn_agent_id=request.user, tn_status=1)
        plist = allocated_property_view.objects.filter(
            agent_id=request.user, pr_is_active=True, pr_is_allocated=False)
        context = {'Tenant_list': Tenant_list, 'plist': plist, }
    return render(request, 'TM_template/Agent/allocate_property.html', context)


def allocate_property(request):
    if request.method == 'POST':
        p = request.POST['page']
        # # print(p)
        # # print(type(p))
        objp = TblProperty.objects.get(id=request.POST['pselect'])
        # print(objp)
        tobj = TblTenant.objects.get(id=request.POST['tselect'])
        # print(tobj)
        try:
            allocation = TblPropertyAllocation.objects.create(pa_property=objp, pa_tenant=tobj, pa_agreement_date=request.POST['start_agreement_date'], pa_agreement_end_date=request.POST[
                'end_agreement_date'], pa_acceptance_latter=request.FILES['pa_agreement_letter'], pa_tenancy_agreement=request.FILES['tenancy_agreement'], pa_final_rent=request.POST['final_rent'], pa_is_allocated=True)
            allocation.save()
            objp.pr_is_allocated = True
            objp.save()
            tobj.tn_status = 3
            tobj.save()
        except Exception as e:
            print("\n\nError: ", e)

        if p == "pdetails":
            return HttpResponseRedirect(reverse(allocated_property_list))
        if p == "tdetails":
            return HttpResponseRedirect(reverse(view_tenants))
    return get_Tenant_list(request)


def deallocate_property(request):
    tid = request.GET['tenant']

    tobj = TblTenant.objects.get(id=tid)
    tobj.tn_status = 0
    tobj.save()
    plist = TblPropertyAllocation.objects.filter(
        pa_tenant=tobj, pa_is_allocated=True)
    # for p in plist:
        # print(p.id)
    TblProperty.objects.get(id=p.id).update(pr_is_allocated=False)
    plist.update(pa_is_allocated=False)

    return HttpResponse("1")


@for_staff
def add_visit(request):
    if request.method == 'GET':
        if 'tid' in request.GET.keys():
            # print(request.GET['tid'])
            tenant = TblTenant.objects.get(id=request.GET['tid'])
            plist = allocated_property_view.objects.filter(
                agent_id=request.user, pr_is_active=True, pr_is_allocated=False)
            context={'tenant':tenant,'plist':plist}
        else:
            tlist = TblTenant.objects.filter(
                tn_is_active=True, tn_agent_id=request.user)
            plist = allocated_property_view.objects.filter(
                    agent_id=request.user, pr_is_active=True, pr_is_allocated=False)
            context={'tlist':tlist,'plist':plist}
        return render(request,'TM_template/Agent/add_visit.html',context)
    if request.method == 'POST':
        tenant=TblTenant.objects.get(id=request.POST['selectedtn'])
        prop=TblProperty.objects.get(id=request.POST['selectedpr'])
        TblVisit.objects.create(vs_tenant=tenant,vs_property=prop,vs_date=request.POST['visitdate'],vs_intrest_status=request.POST['selectedin'])
        return HttpResponseRedirect(reverse(view_tenants))
    else:
        agenthome(request)
