from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import ShortUrl, ShortUrlForm
import urllib.parse

# Create your views here.
def index(request):
    """
    Return a form (Django template) to create new short URL,
    as well as resulting URL or error
    """

    return render(
        request,
        "short_urls/index.html",
        {
            "formset": ShortUrlForm(),
            "host": request.get_host(),
        },
    )


def redirect_short_url(request, slug):
    """
    Redirects to original URL from short URL
    """
    short_url = get_object_or_404(ShortUrl, slug=slug)
    return HttpResponseRedirect(short_url.original_url)


def url_form(request):
    """
    Process the form and return the short URL, or an error if not valid
    """
    query_params = {}

    if request.method == "POST":
        formset = ShortUrlForm(request.POST)
        if formset.is_valid():
            # If original_url is NOT already known, save object and return new slug
            short_url = formset.save(commit=False)
            short_url.slug = ShortUrl.generate_hashed_short_slug()
            short_url.save()
            query_params["slug"] = short_url.slug

        # If the form is not valid OR the URL is already known
        else:
            try:
                query_params["slug"] = ShortUrl.objects.get(
                    original_url=request.POST["original_url"]
                ).slug
            except ShortUrl.DoesNotExist:
                query_params["not_valid"] = request.POST["original_url"]

    return HttpResponseRedirect(
        f"{reverse('short_urls:index')}?{urllib.parse.urlencode(query_params)}"
    )
