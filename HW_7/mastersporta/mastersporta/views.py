from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def auth_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('shop'))
    else:
        return render(request, 'auth.html')
