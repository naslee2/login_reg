from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
def index(request):
        return render(request, 'index.html')

def success(request):
    if 'id' not in request.session:
        return redirect('/login_reg')
    else:
        return render(request, 'success.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.validator(request.POST)
        if 'valid_user' in errors:
            request.session['register_email']=request.POST['email']
            request.session['id']= errors['valid_user'].id
            return redirect('/login_reg/success')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/login_reg')
    else:
        return redirect('/login_reg')

def login(request):
    if request.method == "POST":
        errors2 = User.objects.validator2(request.POST)
        if 'success' in errors2:
            request.session['first_name'] = errors2['success'].first_name
            request.session['login_email'] = errors2['success'].email
            request.session['id']= errors2['success'].id
            return redirect('/login_reg/success')
        else:
            for tag, error in errors2.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/login_reg')
    else:
        return redirect('/login_reg')

