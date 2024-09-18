from django.shortcuts import render

def get_clinics_page(request):
    return render(request, 'clinics.html')


def get_doctors_page(request):
    return render(request, 'doctors.html')


def get_patients_page(request):
    return render(request, 'patients.html')
