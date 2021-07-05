from django.core.files.base import ContentFile
from django.shortcuts import render
from .models import *
from .forms import *
# Create your views here.


def home(request):
    doctors_count = Expert.objects.all().filter(type='1').count()
    doctors = Expert.objects.all().filter(type='1')
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'count': doctors_count,
        'doctors': doctors, 
        'form': form,
        'patients' : Patient.objects.all(),
        'experts': Expert.objects.all()
        }
    return render(request, 'index.html', context)
