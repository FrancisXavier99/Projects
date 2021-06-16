from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Member

def index(request):
    if request.method == 'POST':

        member = Member(email=request.POST['email'], password=request.POST['password'], firstname=request.POST['firstname'],
                        lastname=request.POST['lastname'])
        if Member.objects.filter(email=request.POST['email']).exists():
            context = {'msg': 'Email already Exists'}
            return render(request, "index.html", context,{form})
        else:
            member.save()
            context = {'msg': 'Registered Succesfully'}
            return render(request, "login.html", context)
    else:
        return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def home(request):
    global member
    if request.method == 'POST':
        if request.method == 'POST':
            if Member.objects.filter(email=request.POST['email'], password=request.POST['password']).exists():
            
                member = Member.objects.get(email=request.POST['email'], password=request.POST['password'])
                return render(request, 'home.html', {'member': member})

            else:
                context = {'msg': 'Invalid Email or password'}
                return render(request, 'login.html', context)
        else:
            if member:
                return render(request, 'home.html', {'member': member})
            else:
                return render(request, 'login.html')

def logout(request):
    return render(request, 'login.html')