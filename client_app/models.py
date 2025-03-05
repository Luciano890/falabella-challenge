from django.db import models

from .enums import IdType

# Create your models here.

class Client(models.Model):
    """Client Model"""
    id_type = models.IntegerField(choices=[(tag.value, tag.name) for tag in IdType])
    id_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def get_id_type_name(self):
        """Devuelve el nombre del Enum correspondiente al id_type."""
        return IdType(self.id_type).name

    def __str__(self):
        return self.name


class ClientShoppings(models.Model):
    """ClientShoppings Model"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f'{self.client.name} - {self.date} - {self.name}'
