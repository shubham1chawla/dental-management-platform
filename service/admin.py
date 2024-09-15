from django.contrib import admin
from .models import Clinic, Doctor, Procedure

# Register your models here.
admin.site.register(Clinic)
admin.site.register(Procedure)
admin.site.register(Doctor)