from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.serializers import serialize
from api.models import Domain
from api.views import DomainViewSet
from api.serializers import DomainSerializer
import json


class APITestCase(TestCase):
    _password = u'password'

    def setUp(self):
        self.client = Client()
        self.private_domain = Domain(name="https://www.google.com.ua/",
                                     is_private=True)
        self.private_domain.save()

        self.public_domain = Domain(name="https://www.yandex.ua/",
                                    is_private=False)
        self.public_domain.save()

        self.user = User.objects.create_user('tt@tt.tt', 'tt@tt.tt',
                                             self._password)
        self.manager = User.objects.create_user('manager', 'qq@qq.qq',
                                                self._password)

    def test_get_list(self):
        """
            GET /api/ domain list
        """
        # check api for anonymous user
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [
            DomainSerializer(i).data for i in Domain.objects.filter(
                is_private=False)])

        # check api for authnticated user
        self.client.force_login(self.user)
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [
            DomainSerializer(i).data for i in Domain.objects.all()])

    def test_get_domain(self):
        """
            GET /api/<id> domain detail
        """
        # check api for anonymous user and private domain
        response = self.client.get('/api/%d/' % self.private_domain.id)
        self.assertEqual(response.status_code, 404)

        # check api for anonymous user and public domain
        response = self.client.get('/api/%d/' % self.public_domain.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), DomainSerializer(
            self.public_domain).data)

        # check api for authenticated user
        self.client.force_login(self.user)
        response = self.client.get('/api/%d/' % self.private_domain.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), DomainSerializer(
            self.private_domain).data)

    def test_create_domain(self):
        """
            POST /api/
        """
        # check api with wrong POST data(empty)
        response = self.client.post('/api/')
        self.assertEqual(response.status_code, 404)

        # check api with wrong POST data(HTTP)
        response = self.client.post('/api/', {'name': 'http://yahoo.com',
                                              'is_private': True})
        self.assertEqual(response.status_code, 404)

        # check api for authenicated user
        domain_data = {'name': 'https://yahoo.com', 'is_private': True}
        self.client.force_login(self.user)
        response = self.client.post('/api/', domain_data)
        self.assertEqual(response.status_code, 404)

        # check api for authenicated user - manager
        self.client.force_login(self.manager)
        response = self.client.post('/api/', domain_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Domain.objects.filter(
            name=domain_data['name'], is_private=domain_data['is_private']
            ).count(), 1)
