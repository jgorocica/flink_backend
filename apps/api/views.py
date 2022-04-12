import logging
from .models import Company
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CompanySerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError

# Create your views here.
class CompanyList(APIView):
    """
        Main class which handles the following HTTP methods:
        GET = Fetch all companies
        POST = Create a new company
    """
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)

    def get(self, request):
        companies = Company.objects.all()
        data = CompanySerializer(companies, many=True)
        return Response(data.data, status=status.HTTP_200_OK)

    def post(self, request):
        serialized = CompanySerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        self.logger.warning(f"Error with the body request")
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyDetail(APIView):
    """
        Main class which handles the following HTTP methods:
        PUT = Update a company by ID / PK
        DELETE = Delete an element by ID / PK
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def get_object(self, id):
        try:
            return Company.objects.get(pk=id)
        except ObjectDoesNotExist as ODNE:
            self.logger.warning(f"An error was raised by: {str(ODNE)}")
            return None

    def get(self, request, id):
        company = self.get_object(id=id)
        serialized = CompanySerializer(company, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        company = self.get_object(id=id)
        serialized = CompanySerializer(company, data=request.data, partial=True)
        try:
            if serialized.is_valid():
                with transaction.atomic():
                    serialized.save()

                return Response(serialized.data, status=status.HTTP_200_OK)
        except IntegrityError as IE:
            self.logger.warning(f"An error was raised by: {str(IE)}")
            return Response(
                {
                    'message': 'Ocurrió un error al momento de procesar la petición'
                },
                status=status.HTTP_400_BAD_REQUEST)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        company = self.get_object(id=id)
        company.delete()
        return Response(status=status.HTTP_200_OK)