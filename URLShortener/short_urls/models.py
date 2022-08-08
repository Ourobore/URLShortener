import string
from django.db import models
from django.forms import ModelForm
from django.core.validators import MinLengthValidator, MaxLengthValidator
from hashids import Hashids

SHORT_URL_LENGTH = 6
SHORT_URL_CHARSET = string.ascii_letters

hashids = Hashids(
    alphabet=SHORT_URL_CHARSET,
    min_length=SHORT_URL_LENGTH,
)

# Create your models here.
class ShortUrl(models.Model):

    slug = models.CharField(
        unique=True,
        blank=False,
        max_length=16,
        validators=[MinLengthValidator(SHORT_URL_LENGTH)],
    )
    original_url = models.URLField(
        unique=True,
        blank=False,
        validators=[MaxLengthValidator(2000)],
    )

    def __str__(self):
        return f"[{self.slug}] : {self.original_url}"

    def generate_hashed_short_slug():
        new_id = 0
        try:
            new_id = ShortUrl.objects.latest("id").id + 1
        finally:
            return hashids.encode(new_id)


class ShortUrlForm(ModelForm):
    class Meta:
        model = ShortUrl
        fields = ["original_url"]
