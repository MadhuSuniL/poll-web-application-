from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User 
from .models import UserDetails
# Create your views here.

def login_page(request):
    try:
        username = request.session['user']
        return redirect('/poll/home')
    except KeyError:
        return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')

def login_handle(request):
    username = request.POST.get('un')
    password = request.POST.get('ps')
    
    user = authenticate(username=username,password=password)
    if user is None:
        return redirect('/register_page')
    request.session['user'] = user.username
    return redirect('/poll/home')

def register_handle(request):
    username = request.POST.get('un')
    email = request.POST.get('email')
    no = request.POST.get('no')
    password = request.POST.get('ps')
    
    user = User.objects.create_user(username=username,email=email,password=password)
    details = UserDetails.objects.create(user=user,ph_no=no)
    return redirect('/')
