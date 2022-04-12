import uuid
from django.db import models

# Create your models here.
class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, verbose_name='Nombre')
    description = models.TextField(max_length=100, verbose_name='Descripción')
    symbol = models.CharField(max_length=10, verbose_name='Símbolo')
    market_values = models.JSONField()