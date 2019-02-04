from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'TM_template/index.html',{'name':"Hanny"})