from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Tutorial

# Create your views here.
def homepage(request):
    return render(request,
        template_name='main/home.html',
        context={'tutorials': Tutorial.objects.all()})

def register(request):
    form = 