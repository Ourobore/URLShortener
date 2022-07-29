from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import ShortUrl

# Create your views here.
def index(request):
    return render(request, 'short_urls/index.html')

def url_form(request):
    # Creating new ShortUrl
    new_short_url = ShortUrl(
        original_url=request.POST['input_url'],
        slug=ShortUrl.generate_random_short_slug(),
    )
    new_short_url.save()
    return HttpResponseRedirect(reverse('short_urls:index'))

def redirect_short_url(request, slug):
    short_url = get_object_or_404(ShortUrl, slug=slug)
    return HttpResponseRedirect(short_url.original_url)