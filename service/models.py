from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
import datetime


class Address(models.Model):
    street_address_1 = models.CharField(max_length=200, null=False, blank=False)
    street_address_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    zipcode = models.CharField(max_length=10, null=False, blank=False, validators=[
        RegexValidator(
            regex = r'^(^[0-9]{5}(?:-[0-9]{4})?$|^$)',
            message = _(u'Must be valid zipcode in formats 12345 or 12345-1234'),
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


    def __str__(self):
        return f'Doctor[name={self.name}]'


class DoctorSpecialty(models.Model):
    class Meta:
        unique_together = ('procedure_id', 'doctor_id')


    procedure_id = models.ForeignKey(Procedure, on_delete=models.CASCADE, null=False)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)


# ISO Weekday
def validate_weekday(value: int):
    if value < 0 or value > 6:
        raise ValidationError(_(f'Weekday must be between 0 and 6'))


class DoctorSchedule(models.Model):
    weekday = models.IntegerField(null=False, validators=[validate_weekday])
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    clinic_id = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=False)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)
    office_address = models.ForeignKey(Address, on_delete=models.RESTRICT, null=False)


def validate_ssn(value):
    ssn_len = len(str(value))
    if ssn_len != 4:
        raise ValidationError(_(f'SSN should be the last 4 digits only'))


class Patient(models.Model):

    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'
        OTHER = 'O'

    name = models.CharField(max_length=120, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT, null=False)
    dob = models.DateField(null=False)
    ssn = models.IntegerField(null=False, blank=False, validators=[validate_ssn])
    gender = models.CharField(max_length=1, choices=Gender.choices, null=False, blank=False)


    def __str__(self):
        return f'Patient[name={self.name}]'
    

class Appointment(models.Model):
    clinic_id = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=False)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    date = models.DateField(null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class AppointmentProcedure(models.Model):
    class Meta:
        unique_together = ('procedure_id', 'appointment_id') 

    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=False)
    procedure_id = models.ForeignKey(Procedure, on_delete=models.RESTRICT, null=False)


class DoctorAppointmentSlot:
    def __init__(self, date: datetime.date, start_time: datetime.time, duration: datetime.timedelta):
        self.date = date
        self.start_time = start_time
        self.end_time = (datetime.datetime.combine(date, start_time) + duration).time()
        self.duration = duration
        self.booked = False
