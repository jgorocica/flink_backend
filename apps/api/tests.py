# Django basic library for testing
from django.test import TestCase

# Rest framework
from rest_framework.test import APIClient
from rest_framework import status

from .models import Company
import json

# Create your tests here.
class CompanyTestCase(TestCase):
    def setUp(self):
        Company.objects.create(
            name="my first company",
            description="This is my first company made with Unittest module",
            symbol="MX-FRST",
            market_values="[123,321,1]"
        )

        Company.objects.create(
            name="my second company",
            description="This is my second company made with Unittest module",
            symbol="MX-SCND",
            market_values="[123,321,3]"
        )
        self.client = APIClient()

    def test_fetch_all_data_from_company(self):
        response = self.client.get('/api/companies/')
        result = json.loads(response.content)

        assert response is not None
        assert response.status_code == status.HTTP_200_OK
        assert len(result) == Company.objects.all().count()

    def test_attempt_create_new_company_successful(self):
        new_company = {
            "name": "My Third Company",
            "description": "This is my Third company, from POST Method",
            "symbol": "MX-SCDD",
            "market_values": "[123,3123,123]"
        }

        response = self.client.post('/api/companies/', data=new_company)
        result = json.loads(response.content)

        assert result is not None
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in result

    def test_attempt_create_new_company_failed(self):
        """
            For this test we're omitting a field in the request - body.
        """
        new_company = {
            "name": "My Fourth Company",
            "description": "This is my Third company, from POST Method",
            "symbol": "MX-SCDD"
        }

        response = self.client.post('/api/companies/', data=new_company)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_company(self):
        company = Company.objects.first()

        name = "This is my UPDATED company"
        description = "This is my UPDATED description"

        company.name = name
        company.description = description
        url = f'/api/companies/{company.id}/'

        response = self.client.put(url, data=company.__dict__)
        result = json.loads(response.content)

        assert result is not None
        assert response.status_code == status.HTTP_200_OK
        assert result['name'] == name
        assert result['description'] == description

    def test_delete_company(self):
        total_elements = Company.objects.all().count()

        company = Company.objects.first()
        url = f'/api/companies/{company.id}/'
        response = self.client.delete(url)

        assert response.status_code == status.HTTP_200_OK
        assert (total_elements - 1) == Company.objects.all().count()