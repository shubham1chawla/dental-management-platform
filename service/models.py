from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField


class Address(models.Model):
    street_address_1 = models.CharField(max_length=200, null=False, blank=False)
    street_address_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    zipcode = models.CharField(max_length=10, null=False, blank=False, validators=[
        RegexValidator(
            regex = r'^(^[0-9]{5}(?:-[0-9]{4})?$|^$)',
            message = 'Must be valid zipcode in formats 12345 or 12345-1234',
        )
    ])


    def __str__(self):
        return f'{self.street_address_1}\n{self.street_address_2 if self.street_address_2 else ''}\n{self.city}, {self.state}\n{self.zipcode}'


class Clinic(models.Model):
    name = models.CharField(max_length=120, unique=True, null=False)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)


    def __str__(self):
        return f'Clinic[name={self.name}]'


class Procedure(models.Model):
    name = models.CharField(max_length=20, unique=True, null=True)

    def __str__(self):
        return f'Procedure[name={self.name}]'


class Doctor(models.Model):
    npi = models.CharField(max_length=10, unique=True, null=False)
    name = models.CharField(max_length=120, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    specialty = models.ForeignKey(Procedure, on_delete=models.RESTRICT, null=False)


    def __str__(self):
        return f'Doctor[name={self.name}]'


class DoctorClinicAffiliation(models.Model):
    class Meta:
        unique_together = (('clinic_id', 'doctor_id'))

    clinic_id = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=False)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)
