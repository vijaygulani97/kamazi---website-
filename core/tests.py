from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Service, Company

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


class CompanyAPITests(APITestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name='Test Company',
            address='123 Test St',
            phone_number='555-1234',
            email='test@company.com',
            website='http://testcompany.com'
        )
        self.list_url = reverse('company-list')
        self.detail_url = reverse('company-detail', kwargs={'pk': self.company.pk})

    def test_create_company(self):
        """
        Ensure we can create a new company object.
        """
        data = {
            'name': 'New Company',
            'address': '456 New Ave',
            'phone_number': '555-5678',
            'email': 'new@company.com',
            'website': 'http://newcompany.com'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 2)

    def test_get_companies(self):
        """
        Ensure we can retrieve a list of companies.
        """
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_company_detail(self):
        """
        Ensure we can retrieve a single company.
        """
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.company.name)

    def test_update_company(self):
        """
        Ensure we can update a company.
        """
        data = {
            'name': 'Updated Company Name',
            'website': 'http://updatedcompany.com'
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, 'Updated Company Name')
        self.assertEqual(self.company.website, 'http://updatedcompany.com')

    def test_delete_company(self):
        """
        Ensure we can delete a company.
        """
        response = self.client.delete(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Company.objects.count(), 0)
