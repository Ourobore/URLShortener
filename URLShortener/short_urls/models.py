import string
import random
from django.db import models
from django.forms import ModelForm
from django.core.validators import MinLengthValidator, MaxLengthValidator

SHORT_URL_LENGTH = 6
SHORT_URL_CHARSET = string.ascii_letters

# Create your models here.
class ShortUrl(models.Model):

    slug = models.CharField(max_length=SHORT_URL_LENGTH, blank=False, validators=[MinLengthValidator(SHORT_URL_LENGTH)])
    original_url = models.URLField(blank=False, validators=[MaxLengthValidator(2000)])

    def __str__(self):
        return self.slug

    def generate_random_short_slug():
        return ''.join(random.choices(SHORT_URL_CHARSET, k=SHORT_URL_LENGTH))

        
class ShortUrlForm(ModelForm):
    class Meta:
        model = ShortUrl
        fields = ['original_url']