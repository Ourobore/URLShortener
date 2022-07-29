from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.conf import settings
from .models import ShortUrl

# Create your views here.
def index(request):
    if slug := request.session.get('slug', None):
        del request.session['slug']
    return render(request, 'short_urls/index.html', {"slug": slug, "host": request.get_host()})

def url_form(request):
    input_url = request.POST['input_url']
    try:
        new_short_url = ShortUrl.objects.get(original_url=input_url)
    except:
        new_short_url = ShortUrl(
            original_url=input_url,
            slug=ShortUrl.generate_random_short_slug(),
        )
        new_short_url.save()
    request.session['slug'] = new_short_url.slug
    return HttpResponseRedirect(reverse('short_urls:index'))

def redirect_short_url(request, slug):
    short_url = get_object_or_404(ShortUrl, slug=slug)
    return HttpResponseRedirect(short_url.original_url)