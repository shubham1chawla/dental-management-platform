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
    context = {
        'doctors': interface.get_doctors(),
    }
    return render(request, 'doctors.html', context=context)


def get_doctor_page(request, doctor_id: int):
    context = {
        'doctor': interface.get_doctor(doctor_id),
        'clinics': interface.get_clinics(doctor_id),
        'specialties': ', '.join(map(lambda x: x.name, interface.get_doctor_specialties(doctor_id))),
        'patients': interface.get_patients(doctor_id=doctor_id),
    }
    return render(request, 'doctor.html', context=context)


def get_add_doctor_page(request):
    return render(request, 'add-doctor.html')


def get_patients_page(request):
    context = {
        'patients': interface.get_patients,
    }
    return render(request, 'patients.html', context=context)
