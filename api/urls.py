from django.urls import path
from . import views

urlpatterns = [
    path('clinics/list', view=views.get_clinics, name='GET Clinics'),
    path('clinics/<int:clinic_id>/doctors/list', view=views.get_doctors_by_clinic_id, name="GET Clinic's Doctors"),
    path('doctors/list', view=views.get_doctors, name='GET Doctors'),
    path('patients/list', view=views.get_patients, name='GET Patients'),
]