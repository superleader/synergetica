from rest_framework.serializers import ModelSerializer

from api.models import Domain


class DomainSerializer(ModelSerializer):

    class Meta:
        model = Domain
