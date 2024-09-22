from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('clinics/', view=views.get_clinics_page, name='Clinics Page'),
    path('clinics/add', view=views.get_add_clinic_page, name='Add Clinic Page'),
    path('clinics/<int:clinic_id>', view=views.get_clinic_page, name='Clinic Page'),
    path('clinics/<int:clinic_id>/update', view=views.get_update_clinic_page, name='Update Clinic Page'),
    path('doctors/', view=views.get_doctors_page, name='Doctors Page'),
    path('doctors/add', view=views.get_add_doctor_page, name='Add Doctor Page'),
    path('doctors/<int:doctor_id>', view=views.get_doctor_page, name='Doctor Page'),
    path('doctors/<int:doctor_id>/update', view=views.get_update_doctor_page, name='Update Doctor Page'),
    path('patients/', view=views.get_patients_page, name='Patients Page'),
    path('patients/add', view=views.get_add_patient_page, name='Add Patient Page'),
    path('patients/<int:patient_id>', view=views.get_patient_page, name='Patient Page'),
    path('patients/<int:patient_id>/update', view=views.get_update_patient_page, name='Update Patient Page'),
    path('patients/<int:patient_id>/schedule', view=views.get_schedule_page, name='Schedule Page'),
    path('', view=RedirectView.as_view(permanent=False, url='clinics/')),
]
