from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Service

class ServiceAPITests(APITestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name='SSL Certificate',
            description='256-bit SSL certificate',
            cost=50.00,
            selling_price=100.00
        )
        self.list_url = reverse('service-list')
        self.detail_url = reverse('service-detail', kwargs={'pk': self.service.pk})

    def test_create_service(self):
        """
        Ensure we can create a new service object.
        """
        data = {
            'name': 'Domain Registration',
            'description': '.com domain registration',
            'cost': 10.00,
            'selling_price': 20.00
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 2)

    def test_get_services(self):
        """
        Ensure we can retrieve a list of services.
        """
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_service_detail(self):
        """
        Ensure we can retrieve a single service.
        """
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.service.name)

    def test_update_service(self):
        """
        Ensure we can update a service.
        """
        data = {
            'name': 'Updated SSL Certificate',
            'selling_price': 120.00
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Updated SSL Certificate')
        self.assertEqual(self.service.selling_price, 120.00)

    def test_delete_service(self):
        """
        Ensure we can delete a service.
        """
        response = self.client.delete(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Service.objects.count(), 0)
