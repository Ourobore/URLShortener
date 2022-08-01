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


def redirect_short_url(request, slug):
    short_url = get_object_or_404(ShortUrl, slug=slug)
    return HttpResponseRedirect(short_url.original_url)


def url_form(request):
    if request.method == "POST":
        # Process the form
        formset = ShortUrlForm(request.POST)
        if formset.is_valid():
            short_url = formset.save(commit=False)

            # If original_url is NOT already known, save object and return new slug
            if not verify_duplicate_original_url(short_url.original_url):
                # Generate a UNIQUE slug
                while not short_url.slug or verify_duplicate_slug(short_url.slug):
                    short_url.slug = ShortUrl.generate_random_short_slug()
                short_url.save()
                request.session["slug"] = short_url.slug

            # Else return existing slug
            else:
                request.session["slug"] = ShortUrl.objects.get(
                    original_url=short_url.original_url
                ).slug

        # If form is not valid
        else:
            request.session["not_valid"] = request.POST["original_url"]

    return HttpResponseRedirect(reverse("short_urls:index"))


#  Logic
def verify_duplicate_original_url(url):
    original_url_list = ShortUrl.objects.values_list("original_url", flat=True)
    if url in list(original_url_list):
        return True
    else:
        return False


def verify_duplicate_slug(slug):
    slug_list = ShortUrl.objects.values_list("slug", flat=True)
    if slug in list(slug_list):
        return True
    else:
        return False
