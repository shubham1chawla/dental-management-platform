from django.urls import path
from . import views

urlpatterns = [
    path('clinics/list', view=views.get_clinics, name='GET Clinics'),
    path('doctors/list', view=views.get_doctors, name='GET Doctors'),
]