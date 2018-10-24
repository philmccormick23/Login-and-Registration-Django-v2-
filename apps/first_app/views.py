from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime 
from django.contrib import messages
from django.utils.crypto import get_random_string
import random
from .models import *
import bcrypt


def index(request):
    dictionary = {
        'users' :  User.objects.all()
    }
    #for u in User.objects.all():
        #u.delete()
    return render(request, 'index.html')

def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags='reg')
        print(errors)
        return redirect('/')
    new_user = User(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=bcrypt.hashpw(request.POST['password'].encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        #Password.objects.create(pwd = password.decode('utf-8') 
        #user = User.objects.get(id = new_user.id)
    )
    new_user.save()
    request.session['id'] = new_user.id 
    request.session['first_name']= new_user.first_name
    return redirect('/success')

def login(request):
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors):
        for key, value in login_errors.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    #request.POST['password'].encode('utf-8')
    
    request.session['id'] = User.objects.filter(email=request.POST['email'])[0].id
    request.session['first_name']= User.objects.get(email=request.POST['email']).first_name 
    return redirect('/success')

def success(request):
    context = {
        'users' : User.objects.all()
    }
    return render(request,'success.html', context)