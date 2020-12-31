from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.conf import settings

from .forms import LoginForm

import json
import urllib


def reg_view(request):
    """Registration page implementation"""
    data = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if form.is_valid() and result['success']:
            form.save()
            return HttpResponseRedirect(reverse('auth'))
        return HttpResponseRedirect(reverse('registr'))
    else:
        form = UserCreationForm()
        data['form'] = form
        return render(request, 'registr.html', data)


def auth_view(request):
    """Authorization page implementation"""
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('shop'))
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(username=cd['username'],
                                    password=cd['password'])
                if user is not None:
                    login(request, user)
                    HttpResponseRedirect(reverse('shop'))
                else:
                    form = LoginForm()
                    return render(request, 'auth.html', {'form': form})
        else:
            form = LoginForm()
        return render(request, 'auth.html', {'form': form})
