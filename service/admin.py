from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Address)
admin.site.register(models.Clinic)
admin.site.register(models.Procedure)
admin.site.register(models.Doctor)
admin.site.register(models.DoctorSchedule)
admin.site.register(models.Patient)
admin.site.register(models.Appointment)
admin.site.register(models.DoctorSpecialty)
admin.site.register(models.AppointmentProcedure)
