from django.contrib import admin
from .models import Address, Clinic, Doctor, DoctorSchedule, Procedure, Patient, Appointment, DoctorSpecialty

# Register your models here.
admin.site.register(Address)
admin.site.register(Clinic)
admin.site.register(Procedure)
admin.site.register(Doctor)
admin.site.register(DoctorSchedule)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(DoctorSpecialty)
