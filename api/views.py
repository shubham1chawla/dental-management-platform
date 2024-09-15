from rest_framework.response import Response
from rest_framework.decorators import api_view
from service.models import Clinic, Doctor, DoctorSchedule, DoctorClinicAffiliation, Patient
from .serializers import ClinicSerializer, DoctorSerializer, DoctorScheduleSerializer, PatientSerializer
from datetime import datetime


@api_view(['GET'])
def get_clinics(_):
    clinics = Clinic.objects.all()
    serializer = ClinicSerializer(clinics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctors_by_clinic_id(_, clinic_id):
    affiliations = DoctorClinicAffiliation.objects.filter(clinic_id=clinic_id)
    doctors = []
    for affiliation in affiliations:
        doctors.append(affiliation.doctor_id)
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctors(_):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_schedule_by_doctor_id(_, doctor_id):
    schedule = DoctorSchedule.objects.filter(doctor_id=doctor_id, date__gt=datetime.now())
    serializer = DoctorScheduleSerializer(schedule, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_patients(_):
    patients = Patient.objects.all()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)
