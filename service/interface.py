from typing import List, Optional
from datetime import datetime
from .models import Clinic, Doctor, DoctorClinicAffiliation, DoctorSchedule, Patient
from .errors import NoClinicFoundError, NoDoctorFoundError


def get_clinics() -> List[Clinic]:
    return Clinic.objects.all()


def get_doctors(clinic_id: Optional[int] = None) -> List[Doctor]:
    if not clinic_id:
        return Doctor.objects.all()
    
    # Checking if clinic exists
    if not Clinic.objects.filter(id=clinic_id).exists():
        raise NoClinicFoundError(clinic_id)
    
    affiliations = DoctorClinicAffiliation.objects.filter(clinic_id=clinic_id)
    return [affiliation.doctor_id for affiliation in affiliations]


def get_schedule(doctor_id: int) -> List[DoctorSchedule]:
    # Checking if doctor exists
    if not Doctor.objects.filter(id=doctor_id).exists():
        raise NoDoctorFoundError(doctor_id)
    
    return DoctorSchedule.objects.filter(doctor_id=doctor_id, date__gt=datetime.now())


def get_patients() -> List[Patient]:
    return Patient.objects.all()