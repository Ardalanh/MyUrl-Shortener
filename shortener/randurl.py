from django.conf import settings
from .models import Urls
import random
import string

min_bound, max_bound = settings.SHORT_URL_LENGTH_BOUNDS


def get_random_url():
    """Generate URL, min and max letters can be assigned from settings."""
    length = random.randint(min_bound, max_bound)
    char = string.ascii_uppercase + string.digits + string.ascii_lowercase
    # if the randomly generated short_id is used then generate next
    while True:
        short_id = ''.join(random.choice(char) for x in range(length))
        try:
            # if the data does not exist, this will raise an exception
            Urls.objects.get(pk=short_id)
        except:
            return short_id
