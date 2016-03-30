from django.contrib.admin import site

from api.models import Domain


site.register(Domain)
