from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from . import serializers
import datetime
from service import interface
from service import errors


@api_view(['GET'])
def get_clinics(_):
    clinics = interface.get_clinics()
    serializer = serializers.ClinicSerializer(clinics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_clinic(_, clinic_id: int) :
    clinic = interface.get_clinic(clinic_id)
    serializer = serializers.ClinicSerializer(clinic)
    return Response(serializer.data)


@api_view(['POST'])
def add_clinic(request):
    clinic = interface.add_clinic(**request.data)
    serializer = serializers.ClinicSerializer(clinic, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_clinic_doctors(_, clinic_id: int):
    try:
        doctors = interface.get_doctors(clinic_id)
    except errors.NoClinicFoundError as error:
        raise NotFound(error)

    serializer = serializers.DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctors(_):
    doctors = interface.get_doctors()
    serializer = serializers.DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctor(_, doctor_id: int) :
    doctor = interface.get_doctor(doctor_id)
    serializer = serializers.DoctorSerializer(doctor)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctor_schedules(_, doctor_id: int):
    try:
        schedule = interface.get_schedules(doctor_id)
    except errors.NoDoctorFoundError as error:
        raise NotFound(error)

    serializer = serializers.DoctorScheduleSerializer(schedule, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctor_appointment_slots(_, doctor_id: int, schedule_date: datetime.date):
    slots = interface.get_doctor_appointment_slots(doctor_id, schedule_date)
    serializer = serializers.DoctorAppointmentSlotSerializer(slots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_patients(_):
    patients = interface.get_patients()
    serializer = serializers.PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_patient(_, patient_id: int) :
    patient = interface.get_patient(patient_id)
    serializer = serializers.PatientSerializer(patient)
    return Response(serializer.data)
