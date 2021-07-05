
from accounts.views import logoutUser
from django.contrib.auth.forms import User
from django.db import connection
from django.http.request import HttpRequest
from GlobalApp.models import Expert, publication , room ,Patient , Poste
from accounts.models import Profile
from .models import est_membre_de , a_comme_contact, message
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def forum_page(request):
    pats = Patient.objects.all()
    exps = Expert.objects.all()
    list = []
    list2 = []
    for pat in pats :
        list.append(pat.user)
    for exp in exps :
        list2.append(exp.user)
    if request.user in list or request.user in list2 :    
        context = {
            'patients' :Patient.objects.all(),
            'experts' : Expert.objects.all(),
            'rooms' : room.objects.all(),
            'postes' : Poste.objects.all(),
            'publications' : publication.objects.all(),
            'est_membre' : est_membre_de.objects.all(),
            'a_contact' : a_comme_contact.objects.all(),
            'profiles' : Profile.objects.all(),
            'relation' : a_comme_contact.objects.all()
        }
        return render(request, "forum.html",context)
    return render(request,"403.html")


#pour lister les amis
@login_required
def forum_page_amis(request,usrname):
    pats = Patient.objects.all()
    exps = Expert.objects.all()
    list = []
    list2 = []
    for pat in pats :
        list.append(pat.user)
    for exp in exps :
        list2.append(exp.user)
    if request.user in list or request.user in list2 :  
        form = messageForm()
        context = {
            'patients' :Patient.objects.all(),
            'experts' : Expert.objects.all(),
            'rooms' : room.objects.all(),
            'messages' : message.objects.all(),
            'contact_selectionne' : User.objects.get(username =usrname),
            'postes' : Poste.objects.all(),
            'publications' : publication.objects.all(),
            'est_membre' : est_membre_de.objects.all(),
            'a_contact' : a_comme_contact.objects.all(),
            'profiles' : Profile.objects.all(),
            'relation' : a_comme_contact.objects.all(),
            'form' : form
        }
        return render(request, "messaging.html",context)
    return render (request,"403.html")    

#pour voir les groupes

@login_required
def forum_page_groupe(request,id):
    pats = Patient.objects.all()
    exps = Expert.objects.all()
    list = []
    list2 = []
    for pat in pats :
        list.append(pat.user)
    for exp in exps :
        list2.append(exp.user)
    if request.user in list or request.user in list2 :  
        context = {
            'patients' :Patient.objects.all(),
            'experts' : Expert.objects.all(),
            'rooms' : room.objects.all(),
            'grp_selectionne' : room.objects.get(pk=id),
            'postes' : Poste.objects.all(),
            'publications' : publication.objects.all(),
            'est_membre' : est_membre_de.objects.all(),
            'a_contact' : a_comme_contact.objects.all(),
            'profiles' : Profile.objects.all(),
            'relation' : a_comme_contact.objects.all()
        }

        return render(request, "forum.html",context)
    return render (request,"403.html")            

#pour publier un message

@login_required
def poste_pub(request, id, pk):
    exps = Expert.objects.all()
    list2 = []
    for exp in exps :
        list2.append(exp.user)
    if  request.user in list2 :  
        groupe = room.objects.get(id=id)
        user = User.objects.get(id=pk)
        the_exp = Expert.objects.get(user = user)
        form = PostForm()

        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                titre = form.cleaned_data['title']
                contenu = form.cleaned_data['body']
                poste = Poste.objects.create(titre=titre, contenu=contenu, publie_par=the_exp)
                poste.save()
                pub = publication.objects.create(publie_dans=groupe, poste_publie=poste)
                pub.save()
        context = {
            'patients' :Patient.objects.all(),
            'experts' : Expert.objects.all(),
            'rooms' : room.objects.all(),
            'grp_selectionne' : room.objects.get(pk=id),
            'postes' : Poste.objects.all(),
            'publications' : publication.objects.all(),
            'est_membre' : est_membre_de.objects.all(),
            'a_contact' : a_comme_contact.objects.all(),
            'profiles' : Profile.objects.all(),
            'relation' : a_comme_contact.objects.all(),
            'form':form
        }
        return render(request, 'forum.html', context)
    return render(request,"403.html")        

#pour envoyer un message

@login_required
def env_message(request, usrname, id):
    pats = Patient.objects.all()
    exps = Expert.objects.all()
    list = []
    list2 = []
    for pat in pats :
        list.append(pat.user)
    for exp in exps :
        list2.append(exp.user)
    if request.user in list  :  
        user = request.user
        de = Patient.objects.get(user=user.id)
        vers = User.objects.get(username=usrname)
        form = messageForm()

        if request.method == 'POST':
            form = messageForm(request.POST)
            if form.is_valid():
                mon_message = form.cleaned_data['message']
                conn = a_comme_contact.objects.get(util_connecte= de,son_contact=vers)
                my_message = message.objects.create(connection = conn , connecte_a_contact =True , msg =  mon_message)
                my_message.save()
        context = {
            'patients' :Patient.objects.all(),
            'experts' : Expert.objects.all(),
            'rooms' : room.objects.all(),
            'messages' : message.objects.all(),
            'contact_selectionne' : User.objects.get(username =usrname),
            'postes' : Poste.objects.all(),
            'publications' : publication.objects.all(),
            'est_membre' : est_membre_de.objects.all(),
            'a_contact' : a_comme_contact.objects.all(),
            'profiles' : Profile.objects.all(),
            'relation' : a_comme_contact.objects.all(),
            'form' : form
        }
        return render(request, 'messaging.html', context)   
    if  request.user in list2 : 
        user = User.objects.get(username=usrname)
        de = Patient.objects.get(user=user)
        vers = User.objects.get(id=id)
        form = messageForm()

        if request.method == 'POST':
            form = messageForm(request.POST)
            if form.is_valid():
                mon_message = form.cleaned_data['message']
                conn = a_comme_contact.objects.get(util_connecte= de,son_contact=vers)
                my_message = message.objects.create(connection = conn , connecte_a_contact =False , msg =  mon_message)
                my_message.save()
        context = {
            'patients' :Patient.objects.all(),
            'experts' : Expert.objects.all(),
            'rooms' : room.objects.all(),
            'messages' : message.objects.all(),
            'contact_selectionne' : User.objects.get(username =usrname),
            'postes' : Poste.objects.all(),
            'publications' : publication.objects.all(),
            'est_membre' : est_membre_de.objects.all(),
            'a_contact' : a_comme_contact.objects.all(),
            'profiles' : Profile.objects.all(),
            'relation' : a_comme_contact.objects.all(),
            'form' : form
        }
        return render(request, 'messaging.html', context)   
    return render(request, "403.html")
