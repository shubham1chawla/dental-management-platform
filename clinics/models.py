from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Clinic(models.Model):
    name = models.CharField(max_length=120, unique=True, null=False)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)
    zipcode = models.CharField(max_length=10, null=False, validators=[
        RegexValidator(
            regex = r'^(^[0-9]{5}(?:-[0-9]{4})?$|^$)',
            message = 'Must be valid zipcode in formats 12345 or 12345-1234',
        )
    ])
    email = models.EmailField(unique=True, null=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)