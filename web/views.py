from django.shortcuts import render
from service import interface


def get_clinics_page(request):
    context = {
        'clinics': interface.get_clinics()
    }
    return render(request, 'clinics.html', context=context)


def get_doctors_page(request):
    return render(request, 'doctors.html')


def get_patients_page(request):
    return render(request, 'patients.html')
