from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('clinics/', view=views.get_clinics_page, name='Clinics Page'),
    path('clinics/add', view=views.get_add_clinic_page, name='Add Clinic Page'),
    path('clinics/<int:clinic_id>', view=views.get_clinic_page, name='Clinic Page'),
    path('doctors/', view=views.get_doctors_page, name='Doctors Page'),
    path('patients/', view=views.get_patients_page, name='Patients Page'),
    path('', view=RedirectView.as_view(permanent=False, url='clinics/')),
]
