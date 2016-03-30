from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_201_CREATED
from django.http import Http404

from api.serializers import DomainSerializer
from api.models import Domain


class DomainViewSet(ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    def create(self, request, *args, **kwargs):
        if request.user.username != 'manager':
            raise Http404
        return super(DomainViewSet, self).create(request, args, kwargs)

    def get_queryset(self):
        queryset = Domain.objects.all()
        if not self.request.user.is_authenticated():
            queryset = queryset.filter(is_private=False)
        return queryset
