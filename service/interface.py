from typing import List, Optional, Final
import datetime
from enum import StrEnum
from django.db.models import Q
from .models import Address, Clinic, Doctor, DoctorSchedule, Patient, Appointment, DoctorAppointmentSlot, Procedure, DoctorSpecialty, AppointmentProcedure
from . import errors


"""
Assuming that slots will be 55 minutes long and will have a 5 minutes buffer between them.
"""
DEFAULT_SLOT_DURATION: Final[datetime.timedelta] = datetime.timedelta(minutes=55)
DEFAULT_SLOT_BUFFER: Final[datetime.timedelta] = datetime.timedelta(minutes=5)


def get_clinics(**kwargs) -> List[Clinic]:

    # Filtering clinics based on doctor
    if 'doctor_id' in kwargs:
        doctor_id = kwargs['doctor_id']
    
        # Checking if doctor exists
        if not Doctor.objects.filter(id=doctor_id).exists():
            raise errors.NoDoctorFoundError(doctor_id)
        
        clinic_ids = DoctorSchedule.objects.filter(doctor_id=doctor_id).values_list('clinic_id', flat=True).distinct()
        return [get_clinic(clinic_id) for clinic_id in clinic_ids]

    # Filtering clinics based on procedure
    if 'procedure_id' in kwargs:
        procedure_id = kwargs['procedure_id']

        # Fetching doctors performing this procedure
        doctors = get_doctors(procedure_id=procedure_id)
        doctor_ids = [doctor.id for doctor in doctors]

        clinic_ids = DoctorSchedule.objects.filter(doctor_id__in=doctor_ids).values_list('clinic_id', flat=True).distinct()
        return [get_clinic(clinic_id) for clinic_id in clinic_ids]

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


def update_clinic(clinic_id, **kwargs) -> Clinic:
    if not clinic_id or not Clinic.objects.filter(id=clinic_id).exists():
        raise errors.NoClinicFoundError(clinic_id)

    clinic = Clinic.objects.get(id=clinic_id)
    address = clinic.address

    Address.objects.update_or_create(kwargs['address'], id=address.id)
    del kwargs['address']
    Clinic.objects.update_or_create(kwargs, id=clinic_id)

    return Clinic.objects.get(id=clinic_id)


def get_doctors(**kwargs) -> List[Doctor]:
    clinic_id = procedure_id = None
    if 'clinic_id' in kwargs:
        clinic_id = kwargs['clinic_id']

        # Checking if clinic exists
        if not Clinic.objects.filter(id=clinic_id).exists():
            raise errors.NoClinicFoundError(clinic_id)
    
    if 'procedure_id' in kwargs:
        procedure_id = kwargs['procedure_id']

        # Checking if procedure exists
        if not Procedure.objects.filter(id=procedure_id).exists():
            raise errors.NoProcedureFoundError(procedure_id)
    
    # Filtering doctors based on clinic and procedure
    if clinic_id and procedure_id:
        doctor_ids = DoctorSchedule.objects.filter(clinic_id=clinic_id).values_list('doctor_id', flat=True).distinct()
        doctor_ids = DoctorSpecialty.objects.filter(procedure_id=procedure_id, doctor_id__in=doctor_ids).values_list('doctor_id', flat=True).distinct()
        return [get_doctor(doctor_id) for doctor_id in doctor_ids]

    # Filtering doctors based on clinic
    if clinic_id:
        doctor_ids = DoctorSchedule.objects.filter(clinic_id=clinic_id).values_list('doctor_id', flat=True).distinct()
        return [get_doctor(doctor_id) for doctor_id in doctor_ids]

    # Filtering doctors based on procedure
    if procedure_id:
        doctor_ids = DoctorSpecialty.objects.filter(procedure_id=procedure_id).values_list('doctor_id', flat=True).distinct()
        return [get_doctor(doctor_id) for doctor_id in doctor_ids]

    return Doctor.objects.all()


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


def update_doctor(doctor_id: int, **kwargs) -> Doctor:
    if not doctor_id or not Doctor.objects.filter(id=doctor_id).exists():
        raise errors.NoDoctorFoundError(doctor_id)

    procedure_ids = kwargs['specialties']
    del kwargs['specialties']

    # Updating doctor's fields
    doctor, _ = Doctor.objects.update_or_create(kwargs, id=doctor_id)
    
    # Deleting old specialties
    doctor_specialties = DoctorSpecialty.objects.filter(doctor_id=doctor_id)
    for specialty in doctor_specialties:
        specialty.delete()

    # Inserting new specialties
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


def get_schedule(id: int) -> DoctorSchedule:
    if not id or not DoctorSchedule.objects.filter(id=id).exists():
        raise errors.NoDoctorScheduleFoundError(id)
    
    return DoctorSchedule.objects.get(id=id)


def add_schedule(**kwargs) -> DoctorSchedule:
    # Checking if doctor already in another clinic
    doctor = kwargs['doctor_id']
    weekday = kwargs['weekday']
    if DoctorSchedule.objects.filter(doctor_id=doctor, weekday=weekday).exists():
        raise errors.DoctorUnavailableError(doctor.id, weekday)

    address = Address(**kwargs['office_address'])
    address.save()
    del kwargs['office_address']

    schedule = DoctorSchedule(office_address=address, **kwargs)
    schedule.save()
    return schedule


def update_schedule(id: int, **kwargs) -> DoctorSchedule:
    if not id or not DoctorSchedule.objects.filter(id=id).exists():
        raise errors.NoDoctorScheduleFoundError(id)
    
    schedule = DoctorSchedule.objects.get(id=id)
    address = schedule.office_address

    Address.objects.update_or_create(kwargs['office_address'], id=address.id)
    del kwargs['office_address']
    DoctorSchedule.objects.update_or_create(kwargs, id=id)

    return DoctorSchedule.objects.get(id=id)


def remove_schedule(id: int):
    if not id or not DoctorSchedule.objects.filter(id=id).exists():
        raise errors.NoDoctorScheduleFoundError(id)
    
    schedule = DoctorSchedule.objects.get(id=id)
    office_address = schedule.office_address
    schedule.delete()
    office_address.delete()


def get_appointment_slots(doctor_id: int, clinic_id: int, date: datetime.date) -> List[DoctorAppointmentSlot]:
    schedules = get_schedules(doctor_id, clinic_id=clinic_id, date=date)
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


def add_appointment(**kwargs) -> Appointment:
    procedure = kwargs['procedure_id']
    del kwargs['procedure_id']

    appointment = Appointment(**kwargs)
    appointment.save()

    appointment_procedure = AppointmentProcedure(appointment_id=appointment, procedure_id=procedure)
    appointment_procedure.save()

    return appointment


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


def add_patient(**kwargs) -> Patient:
    # Saving the address details
    address = Address(**kwargs['address'])
    address.save()

    # Saving the patient details
    del kwargs['address']
    patient = Patient(**kwargs, address=address)
    patient.save()
    return patient


def update_patient(patient_id: int, **kwargs) -> Patient:
    if not patient_id or not Patient.objects.filter(id=patient_id).exists():
        raise errors.NoPatientFoundError(patient_id)

    patient = Patient.objects.get(id=patient_id)
    address = patient.address

    Address.objects.update_or_create(kwargs['address'], id=address.id)
    del kwargs['address']
    Patient.objects.update_or_create(kwargs, id=patient_id)

    return Patient.objects.get(id=patient_id)


class PatientAppointmentMode(StrEnum):
    ALL = 'all'
    LAST = 'last'
    NEXT = 'next'


def get_patient_appointments(id: int, mode: Optional[PatientAppointmentMode] = PatientAppointmentMode.ALL) -> List[Appointment]:
    # Checking if patient exists
    if not id or not Patient.objects.filter(id=id).exists():
        raise errors.NoPatientFoundError(id)
    
    if mode == PatientAppointmentMode.ALL:
        return Appointment.objects.filter(patient_id=id).order_by('date', 'start_time')
    
    # getting current date
    date = datetime.date.today()

    if mode == PatientAppointmentMode.LAST:
        return Appointment.objects.filter(patient_id=id, date__lt=date).order_by('date', 'end_time').reverse()
    
    if mode == PatientAppointmentMode.NEXT:
        return Appointment.objects.filter(patient_id=id, date__gte=date).order_by('date', 'start_time')

    return []


def get_procedures(appointment_id: Optional[int] = None) -> List[Procedure]:
    if not appointment_id:
        return Procedure.objects.all().order_by('name')

    procedure_ids = AppointmentProcedure.objects.filter(appointment_id=appointment_id).values_list('procedure_id', flat=True).distinct()
    return [Procedure.objects.get(id=procedure_id) for procedure_id in procedure_ids]


def get_procedure(id: int) -> Procedure:
    if not id or not Procedure.objects.filter(id=id).exists():
        raise errors.NoProcedureFoundError(id)
    
    return Procedure.objects.get(id=id)
