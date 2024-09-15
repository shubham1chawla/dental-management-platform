from django.contrib import admin
from .models import Address, Clinic, Doctor, Procedure, DoctorClinicAffiliation, Patient

# Register your models here.
admin.site.register(Address)
admin.site.register(Clinic)
admin.site.register(Procedure)
admin.site.register(Doctor)
admin.site.register(DoctorClinicAffiliation)
admin.site.register(Patient)
