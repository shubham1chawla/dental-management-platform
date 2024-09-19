from typing import List, Optional, Final
import datetime
from django.db.models import Q
from .models import Address, Clinic, Doctor, DoctorSchedule, Patient, Appointment, DoctorAppointmentSlot, Procedure, DoctorSpecialty
from . import errors


"""
Assuming that slots will be 55 minutes long and will have a 5 minutes buffer between them.
"""
DEFAULT_SLOT_DURATION: Final[datetime.timedelta] = datetime.timedelta(minutes=55)
DEFAULT_SLOT_BUFFER: Final[datetime.timedelta] = datetime.timedelta(minutes=5)


def get_clinics(doctor_id: Optional[int] = None) -> List[Clinic]:
    if not doctor_id:
        return Clinic.objects.all()
    
    # Checking if doctor exists
    if not Doctor.objects.filter(id=doctor_id).exists():
        raise errors.NoDoctorFoundError(doctor_id)
    
    clinic_ids = DoctorSchedule.objects.filter(doctor_id=doctor_id).values_list('clinic_id', flat=True).distinct()
    return [get_clinic(clinic_id) for clinic_id in clinic_ids]


def get_clinic(id: int) -> Clinic:
    if not id or not Clinic.objects.filter(id=id).exists():
        raise errors.NoClinicFoundError(id)
    
    return Clinic.objects.get(id=id)


def add_clinic(**kwargs) -> Clinic:
    # Saving the address details
    address = Address(**kwargs['address'])
    address.save()

    # Saving the clinic details
    del kwargs['address']
    clinic = Clinic(**kwargs, address=address)
    clinic.save()
    return clinic


def get_doctors(clinic_id: Optional[int] = None) -> List[Doctor]:
    if not clinic_id:
        return Doctor.objects.all()
    
    # Checking if clinic exists
    if not Clinic.objects.filter(id=clinic_id).exists():
        raise errors.NoClinicFoundError(clinic_id)
    
    doctor_ids = DoctorSchedule.objects.filter(clinic_id=clinic_id).values_list('doctor_id', flat=True).distinct()
    return [get_doctor(doctor_id) for doctor_id in doctor_ids]


def get_doctor(id: int) -> Doctor:
    if not id or not Doctor.objects.filter(id=id).exists():
        raise errors.NoDoctorFoundError(id)
    
    return Doctor.objects.get(id=id)


def add_doctor(**kwargs) -> Doctor:
    procedure_ids = kwargs['specialties']
    del kwargs['specialties']

    # Saving the doctor details
    doctor = Doctor(**kwargs)
    doctor.save()

    # Saving specialties
    for procedure_id in procedure_ids:
        procedure = Procedure.objects.get(id=procedure_id)
        specialty = DoctorSpecialty(doctor_id=doctor, procedure_id=procedure)
        specialty.save()

    return doctor


def get_doctor_specialties(id: int) -> List[Procedure]:
    if not id or not Doctor.objects.filter(id=id).exists():
        raise errors.NoDoctorFoundError(id)
    
    procedure_ids = DoctorSpecialty.objects.filter(doctor_id=id).values_list('procedure_id', flat=True).distinct()
    return [Procedure.objects.get(id=procedure_id) for procedure_id in procedure_ids]


def get_schedules(doctor_id: int, **kwargs) -> List[DoctorSchedule]:
    # Checking if doctor exists
    if not Doctor.objects.filter(id=doctor_id).exists():
        raise errors.NoDoctorFoundError(doctor_id)
    
    if 'date' not in kwargs and 'clinic_id' not in kwargs:
        return DoctorSchedule.objects.filter(doctor_id=doctor_id)
    
    filters = {
        'doctor_id': doctor_id
    }

    if 'date' in kwargs and isinstance(kwargs['date'], datetime.date):
        date = kwargs['date']

        # Calculating the ISO weekday
        filters['weekday'] = date.weekday()

    if 'clinic_id' in kwargs and isinstance(kwargs['clinic_id'], int):
        filters['clinic_id'] = kwargs['clinic_id']

    return DoctorSchedule.objects.filter(**filters).order_by('start_time')


def get_doctor_appointment_slots(doctor_id: int, date: datetime.date) -> List[DoctorAppointmentSlot]:
    schedules = get_schedules(doctor_id, date=date)
    if not schedules:
        return []

    # Looping over schedule to find appointment slots
    slots = []
    for schedule in schedules:
        time = schedule.start_time
        while time < schedule.end_time:
            slot = DoctorAppointmentSlot(date, time, DEFAULT_SLOT_DURATION)

            # Checking if the slot is available
            doctor_criterion = Q(doctor_id=doctor_id, date=date)
            start_time_criterion = Q(start_time__lte=slot.start_time, end_time__gte=slot.start_time)
            end_time_criterion = Q(start_time__lte=slot.end_time, end_time__gte=slot.end_time)
            slot.booked = Appointment.objects.filter(doctor_criterion & (start_time_criterion | end_time_criterion)).exists()
            slots.append(slot)

            # Calculating next slot start time
            time = (datetime.datetime.combine(date, slot.end_time) + DEFAULT_SLOT_BUFFER).time()

    return slots


def get_patients(**kwargs) -> List[Patient]:
    if 'clinic_id' not in kwargs and 'doctor_id' not in kwargs:
        return Patient.objects.all()

    clinic = doctor = None
    filters = {}
    
    # Checking if clinic ID provided
    if 'clinic_id' in kwargs:
        clinic = get_clinic(kwargs['clinic_id'])
        filters['clinic_id'] = clinic.id

    # Checking if doctor ID provided
    if 'doctor_id' in kwargs:
        doctor = get_doctor(kwargs['doctor_id'])
        filters['doctor_id'] = doctor.id

    patient_ids = Appointment.objects.filter(**filters).values_list('patient_id', flat=True).distinct()
    return [get_patient(id) for id in patient_ids]


def get_patient(id: int) -> Patient:
    if not id or not Patient.objects.filter(id=id).exists():
        raise errors.NoPatientFoundError(id)
    
    return Patient.objects.get(id=id)


def get_procedures() -> List[Procedure]:
    return Procedure.objects.all().order_by('name')
