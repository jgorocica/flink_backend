from rest_framework import serializers
from apps.api.models import Company

class CompanySerializer(serializers.ModelSerializer):
    """
        Handle the model instances for Company
        to native Python data types.
    """
    class Meta:
        model = Company
        fields = '__all__'