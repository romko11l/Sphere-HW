from django.http import HttpResponseRedirect
from django.urls import reverse

def redirect(request):
    """Redirect to .../shop/"""
    return HttpResponseRedirect(reverse('shop'))
