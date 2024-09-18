from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('clinics/', view=views.get_clinics_page, name='Clinics Page'),
    path('doctors/', view=views.get_doctors_page, name='Doctors Page'),
    path('patients/', view=views.get_patients_page, name='Patients Page'),
    path('', view=RedirectView.as_view(permanent=False, url='clinics/')),
]
