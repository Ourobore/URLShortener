import string
import random
from django.db import models

SHORT_URL_LENGTH = 6
SHORT_URL_CHARSET = string.ascii_letters

# Create your models here.
class ShortUrl(models.Model):
    original_url = models.URLField()
    short_url = models.URLField()

    def generate_random_short_url():
        return ''.join(random.choices(SHORT_URL_CHARSET, k=SHORT_URL_LENGTH))