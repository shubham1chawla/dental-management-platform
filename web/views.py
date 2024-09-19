from django.shortcuts import render
from service import interface


def get_clinics_page(request):
    context = {
        'clinics': interface.get_clinics()
    }
    return render(request, 'clinics.html', context=context)


def get_clinic_page(request, clinic_id: int):
    context = {
        'clinic': interface.get_clinic(clinic_id),
        'doctors': interface.get_doctors(clinic_id),
    }
    return render(request, 'clinic.html', context=context)


def get_add_clinic_page(request):
    return render(request, 'add-clinic.html')


def get_doctors_page(request):
    return render(request, 'doctors.html')


def get_patients_page(request):
    return render(request, 'patients.html')
