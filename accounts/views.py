from django import utils
from forum.models import *
from GlobalApp.models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import RegisterForm
from django.contrib.auth.models import Group
from django.contrib.admin.views.decorators import staff_member_required
from accounts.models import Profile
from django.views.decorators.csrf import csrf_protect

# Create your views here.


def home(request):

    return render(request, 'index.html')


@staff_member_required
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # à changer ==> patient . create()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Patients')
            user.groups.add(group)

            return redirect('login')
    return render(request, 'register.html', {'form': form})


@csrf_protect
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login_user(request, user)
                return redirect('home')
            else:
                return render(request, 'account.html')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    # return redirect('login')
    return redirect('home')


def profile_view(request):
    pats = Patient.objects.all()
    list = []
    for pat in pats:
        list.append(pat.user)
    if request.user in list :        
        context = {
            'profiles' : Profile.objects.all()
        }
        return render(request, "profil.html", context)
    return render(request,"403.html")        


def my_info(request,id):
    pats = Patient.objects.all()
    list = []
    for pat in pats:
        list.append(pat.user)
    if request.user in list :        
        patient = get_object_or_404(User, pk=id)
        pat = get_object_or_404(Patient, user = patient)
        context = {
            'usrname': patient.username,
            'first': patient.first_name,
            'last': patient.last_name,
            'naissance' : pat.dateNaissance.date,
            'sexe' : pat.sexe
        }
        return render(request,"my_info.html",context)
    return render(request,"403.html")        

def experts(request,id):
    pats = Patient.objects.all()
    list = []
    for pat in pats:
        list.append(pat.user)
    if request.user in list :         
        user = User.objects.get(id=id)
        pat = Patient.objects.get(user = user)
        experts = a_comme_contact.objects.all().filter(util_connecte = pat)
        all_experts = Expert.objects.all()
        context ={
            'experts': experts,
            'all_experts' : all_experts
        }
        return render(request,"experts.html",context)
    return render(request,"403.html")        

def amis(request,id):
    pats = Patient.objects.all()
    list = []
    for pat in pats:
        list.append(pat.user)
    if request.user in list :        
        user = User.objects.get(id=id)
        pat = Patient.objects.get(user = user)
        amis = a_comme_contact.objects.all().filter(util_connecte = pat)
        all_amis = Patient.objects.all()
        context ={
            'amis': amis,
            'all_amis' : all_amis
        }
        return render(request,"amis.html",context)
    return render(request,"403.html")        

def groupes(request,id):
    pats = Patient.objects.all()
    list = []
    for pat in pats:
        list.append(pat.user)
    if request.user in list :     
        user = User.objects.get(id=id)
        pat = Patient.objects.get(user=user)
        groupes = est_membre_de.objects.filter(pat = pat)
        context={
            'groupes' : groupes
        }
        return render(request,"groupes.html",context)   
    return render(request,"403.html")         
