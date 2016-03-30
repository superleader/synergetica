from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from api.views import DomainViewSet

router = routers.DefaultRouter()
router.register(r'api', DomainViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
