from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import ShortUrl, ShortUrlForm

# Create your views here.
def index(request):
    """
    Return a form (Django template) to create new short URL,
    and also resulting URL or error
    """
    # Get previous slug / error
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
    if request.method == "POST":
        formset = ShortUrlForm(request.POST)
        if formset.is_valid():
            # If original_url is NOT already known, save object and return new slug
            short_url = formset.save(commit=False)
            short_url.slug = ShortUrl.generate_hashed_short_slug()
            short_url.save()
            request.session["slug"] = short_url.slug

        # If the form is not valid OR the URL is already known
        else:
            try:
                existing_short_url = ShortUrl.objects.get(
                    original_url=request.POST["original_url"]
                )
                request.session["slug"] = existing_short_url.slug
            except ShortUrl.DoesNotExist:
                request.session["not_valid"] = request.POST["original_url"]

    return HttpResponseRedirect(reverse("short_urls:index"))
