from django.contrib.auth.models import User
from django.shortcuts import render
from .models import *
from .forms import *
from textblob import TextBlob
from GlobalApp.models import *
import random


# Create your views here.
def randomMotivate(a) :
    if a == 0 :
        etat_normal = [
            'Try to be more optimistic',
            'That\'s great !! Have a nice day ',
            ' Have a great day ',
            'Have a great week !!',
            'Be creative !!',
            'Try to do something that will make you Happier .',
            ]
        return random.choice(etat_normal)
    elif a > 0 :
        etat_positive = [
            'That\'s fantastic !!',
            'That\'s awesome !',
            'That\'s GREAAAT !!',
            'That\'s amazing !'
            ]
        return random.choice(etat_positive)
    else :
        etat_negative = [
            'It\'s ok you\'re gonna be alright.',
            'Try talking with Lora .',
            'You can always be better .',
            'Always say AlHamdolillah',
        ]
        return random.choice(etat_negative)

def AnalyseData(request,id):
    pats = Patient.objects.all()
    list = []
    for pat in pats :
        list.append(pat.user)
    if request.user in list: 

        form = dataForm()
        txt = ''
        result = ''
        user1 = User.objects.get(id = id )
        albert = User.objects.get(username = 'Albert')
        pat = Patient.objects.get(user=user1)
        pat_a = Patient.objects.get(user=albert)
        if request.method == 'POST':
            form = dataForm(request.POST)
            if form.is_valid():
                txt = form.cleaned_data['texte']
                blob = TextBlob(txt)
                polar = blob.sentiment.polarity
                obj = DataSaisi.objects.create(user=pat, texte=txt, to=albert)
                obj.save()
                obj1 = DataSaisi.objects.create(user=pat_a, texte=randomMotivate(polar), to=user1)
                obj1.save()
        context = {
            'form': form,
            'dataAnalyzed' : DataSaisi.objects.all().order_by('creation_time'),
            'pat_a' : pat_a,
            }
        return render(request, "Analysis.html", context)
    return render(request,"403.html")