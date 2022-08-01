from django.test import TestCase

from .models import ShortUrl, ShortUrlForm

# Create your tests here.
class ShortUrlModelTests(TestCase):
    pass


class IndexViewTests(TestCase):
    pass


class RedirectShortUrlTests(TestCase):
    def test_short_url_exists(self):
        url = "https://djangoproject.com/"
        response_post = self.client.post("/url_form", data={"original_url": url})
        slug = ShortUrl.objects.get(original_url=url).slug
        response_get = self.client.get("/" + slug)
        self.assertEqual(response_get.status_code, 302)

    def test_short_url_does_not_exists(self):
        slug = "xxxxxx"
        response_get = self.client.get("/" + slug)
        self.assertEqual(response_get.status_code, 404)


class UrlFormViewTests(TestCase):
    def test_original_url_already_exists(self):
        """
        If original_url already exists, must return the existing slug,
        and do not create a new entry in database
        """
        url = "https://google.com"
        response = self.client.post("/url_form", data={"original_url": url})
        self.assertEqual(ShortUrl.objects.all().count(), 1)
        response_two = self.client.post("/url_form", data={"original_url": url})
        self.assertEqual(ShortUrl.objects.all().count(), 1)
