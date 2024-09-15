from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from .serializers import ClinicSerializer, DoctorSerializer, DoctorScheduleSerializer, PatientSerializer
from service import interface
from service import errors


@api_view(['GET'])
def get_clinics(_):
    clinics = interface.get_clinics()
    serializer = ClinicSerializer(clinics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctors_by_clinic_id(_, clinic_id: int):
    try:
        doctors = interface.get_doctors(clinic_id)
    except errors.NoClinicFoundError as error:
        raise NotFound(error)

    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctors(_):
    doctors = interface.get_doctors()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_schedule_by_doctor_id(_, doctor_id: int):
    try:
        schedule = interface.get_schedule(doctor_id)
    except errors.NoDoctorFoundError as error:
        raise NotFound(error)

    serializer = DoctorScheduleSerializer(schedule, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_patients(_):
    patients = interface.get_patients()
    serializer = PatientSerializer(patients, many=True)
    return Response(serializer.data)
