from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegistrationForm, AccountAuthenticationForm
from django.contrib.auth.decorators import login_required



# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            account = form.save()
            username = form.cleaned_data.get('username')
            #email = form.cleaned_data.get('email')
            #password1 = form.cleaned_data.get('password')
            #account = authenticate(email=email, password=password1)
            login(request, account)
            return redirect('home:homepage')
        else:
            context['registration_form'] = form
    else: # GET REQUEST
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)


def log_out(request):
    logout(request)
    return redirect('/')


def log_in(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('/')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                next_page = request.POST.get('next', '/')
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return redirect('/')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, 'account/login.html', context)


@login_required(login_url='/login')
def account_view(request):
    context = {}
    context['account'] = request.user
    return render(request, 'account/account.html', context)
