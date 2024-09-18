from typing import List, Optional, Final
import datetime
from django.db.models import Q
from .models import Address, Clinic, Doctor, DoctorClinicAffiliation, DoctorSchedule, Patient, Appointment, DoctorAppointmentSlot
from . import errors


"""
Assuming that slots will be 55 minutes long and will have a 5 minutes buffer between them.
"""
DEFAULT_SLOT_DURATION: Final[datetime.timedelta] = datetime.timedelta(minutes=55)
DEFAULT_SLOT_BUFFER: Final[datetime.timedelta] = datetime.timedelta(minutes=5)


def get_clinics() -> List[Clinic]:
    return Clinic.objects.all()


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
    
    affiliations = DoctorClinicAffiliation.objects.filter(clinic_id=clinic_id)
    return [affiliation.doctor_id for affiliation in affiliations]


def get_doctor(id: int) -> Doctor:
    if not id or not Doctor.objects.filter(id=id).exists():
        raise errors.NoDoctorFoundError(id)
    
    return Doctor.objects.get(id=id)


def get_schedules(doctor_id: int, date: Optional[datetime.date] = None) -> List[DoctorSchedule]:
    # Checking if doctor exists
    if not Doctor.objects.filter(id=doctor_id).exists():
        raise errors.NoDoctorFoundError(doctor_id)
    
    if not date:
        return DoctorSchedule.objects.filter(doctor_id=doctor_id, date__gte=datetime.date.today())
    return DoctorSchedule.objects.filter(doctor_id=doctor_id, date=date).order_by('start_time')


def get_doctor_appointment_slots(doctor_id: int, date: datetime.date) -> List[DoctorAppointmentSlot]:
    schedules = get_schedules(doctor_id, date)
    if not schedules:
        return []

    # Looping over schedule to find appointment slots
    slots = []
    for schedule in schedules:
        time = schedule.start_time
        while time < schedule.end_time:
            slot = DoctorAppointmentSlot(schedule.date, time, DEFAULT_SLOT_DURATION)

            # Checking if the slot is available
            doctor_criterion = Q(doctor_id=doctor_id, date=schedule.date)
            start_time_criterion = Q(start_time__lte=slot.start_time, end_time__gte=slot.start_time)
            end_time_criterion = Q(start_time__lte=slot.end_time, end_time__gte=slot.end_time)
            slot.booked = Appointment.objects.filter(doctor_criterion & (start_time_criterion | end_time_criterion))
            slots.append(slot)

            # Calculating next slot start time
            time = (datetime.datetime.combine(date, slot.end_time) + DEFAULT_SLOT_BUFFER).time()

    return slots


def get_patients() -> List[Patient]:
    return Patient.objects.all()


def get_patient(id: int) -> Patient:
    if not id or not Patient.objects.filter(id=id).exists():
        raise errors.NoPatientFoundError(id)
    
    return Patient.objects.get(id=id)
