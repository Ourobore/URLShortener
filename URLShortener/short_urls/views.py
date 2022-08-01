from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import ShortUrl, ShortUrlForm

# Create your views here.
def index(request):
    # Get previous slug
    if slug := request.session.get("slug", None):
        del request.session["slug"]
    if not_valid := request.session.get("not_valid", None):
        del request.session["not_valid"]

    return render(
        request,
        "short_urls/index.html",
        {
            "formset": ShortUrlForm(),
            "slug": slug,
            "not_valid": not_valid,
            "host": request.get_host(),
        },
    )


def url_form(request):
    if request.method == "POST":
        # Process the form
        formset = ShortUrlForm(request.POST)
        if formset.is_valid():
            new_short_url = formset.save(commit=False)
            new_short_url.slug = ShortUrl.generate_random_short_slug()
            new_short_url.save()
            request.session["slug"] = new_short_url.slug
        else:
            request.session["not_valid"] = request.POST["original_url"]

    return HttpResponseRedirect(reverse("short_urls:index"))


def redirect_short_url(request, slug):
    short_url = get_object_or_404(ShortUrl, slug=slug)
    return HttpResponseRedirect(short_url.original_url)
