from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template.defaulttags import register
from service import interface


@register.filter
def get_range(value):
    return range(value)


def get_clinics_page(request):
    context = {
        'clinics': interface.get_clinics()
    }
    return render(request, 'clinics.html', context=context)


def get_clinic_page(request, clinic_id: int):
    context = {
        'clinic': interface.get_clinic(clinic_id),
        'doctors': interface.get_doctors(clinic_id=clinic_id),
    }
    return render(request, 'clinic.html', context=context)


def get_update_clinic_page(request, clinic_id: int):
    context = {
        'clinic': interface.get_clinic(clinic_id),
    }
    return render(request, 'update-clinic.html', context=context)


def get_add_clinic_page(request):
    return render(request, 'add-clinic.html')


def get_add_affiliations_page(request, clinic_id: int):
    context = {
        'clinic': interface.get_clinic(clinic_id),
        'doctors': interface.get_doctors(),
    }
    return render(request, 'add-affiliations.html', context=context)


def get_update_affiliations_page(request, clinic_id: int, doctor_id: int):
    context = {
        'clinic': interface.get_clinic(clinic_id),
        'doctor': interface.get_doctor(doctor_id),
    }
    return render(request, 'update-affiliations.html', context=context)


def get_doctors_page(request):
    context = {
        'doctors': interface.get_doctors(),
    }
    return render(request, 'doctors.html', context=context)


def get_doctor_page(request, doctor_id: int):
    context = {
        'doctor': interface.get_doctor(doctor_id),
        'clinics': interface.get_clinics(doctor_id=doctor_id),
        'specialties': ', '.join(map(lambda x: x.name, interface.get_doctor_specialties(doctor_id))),
        'patients': interface.get_patients(doctor_id=doctor_id),
    }
    return render(request, 'doctor.html', context=context)


def get_update_doctor_page(request, doctor_id: int):
    context = {
        'doctor': interface.get_doctor(doctor_id),
    }
    return render(request, 'update-doctor.html', context=context)


def get_add_doctor_page(request):
    return render(request, 'add-doctor.html')


def get_patients_page(request):
    context = {
        'patients': interface.get_patients,
    }
    return render(request, 'patients.html', context=context)


def get_update_patient_page(request, patient_id: int):
    context = {
        'patient': interface.get_patient(patient_id),
    }
    return render(request, 'update-patient.html', context=context)


def get_add_patient_page(request):
    return render(request, 'add-patient.html')


def get_patient_page(request, patient_id: int):
    next_appointments = interface.get_patient_appointments(patient_id, interface.PatientAppointmentMode.NEXT)
    next_appointment_procedures = None
    if next_appointments:
        next_appointment_procedures = interface.get_procedures(next_appointments[0].id)
        next_appointment_procedures = ', '.join(map(lambda x: x.name, next_appointment_procedures))
    context = {
        'patient': interface.get_patient(patient_id),
        'appointments': interface.get_patient_appointments(patient_id),
        'next_appointment': next_appointments[0] if next_appointments else None,
        'next_appointment_procedures': next_appointment_procedures,
    }
    return render(request, 'patient.html', context=context)


def get_schedule_page(request, patient_id: int):
    context = {
        'patient': interface.get_patient(patient_id),
        'procedures': interface.get_procedures(),
    }
    return render(request, 'schedule.html', context=context)


def get_login(request):
    user = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(to='/clinics', permanent=False)
        else:
            messages.success(request, ('No user found with the specified credentials...'))
    return render(request, 'login.html')
