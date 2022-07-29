from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'short_urls/index.html')

def url_form(request):
    return HttpResponseRedirect(reverse('short_urls:index'))