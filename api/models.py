from django.db.models import Model, URLField, BooleanField

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from requests import get, ConnectionError


class HTTPSValidator(object):

    def __call__(self, value):
        if value[:5] != 'https':
            raise ValidationError("URL must start with https")
        try:
            if get(value).status_code != 200:
                raise ValidationError("URL must return status code 200")
        except ConnectionError:
            raise ValidationError("URL must be real")


class Domain(Model):
    name = URLField(unique=True, validators=[HTTPSValidator()])
    is_private = BooleanField()

    def __unicode__(self):
        return self.name
