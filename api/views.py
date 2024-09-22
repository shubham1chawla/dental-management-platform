from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from . import serializers
import datetime
import json
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


@csrf_exempt
def add_clinic(request: HttpRequest) -> HttpResponse:
    data = json.loads(request.body)

    serializer = serializers.ClinicSerializer(data=data)
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    serializer = serializers.AddressSerializer(data=data['address'])
    if not serializer.is_valid():
        return HttpResponseBadRequest()

    clinic = interface.add_clinic(**data)
    serializer = serializers.ClinicSerializer(clinic, many=False)
    return HttpResponse(serializer.data)


@csrf_exempt
def update_clinic(request: HttpRequest, clinic_id: int) -> HttpResponse:
    data = json.loads(request.body)

    clinic = interface.get_clinic(clinic_id)
    serializer = serializers.ClinicSerializer(clinic, data=data)
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    serializer = serializers.AddressSerializer(clinic.address, data=data['address'])
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    clinic = interface.update_clinic(clinic_id, **data)
    serializer = serializers.ClinicSerializer(clinic, many=False)
    return HttpResponse(serializer.data)   


@api_view(['GET'])
def get_clinic_doctors(_, clinic_id: int):
    try:
        doctors = interface.get_doctors(clinic_id=clinic_id)
    except errors.NoClinicFoundError as error:
        raise NotFound(error)

    serializer = serializers.DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_clinic_doctor_schedules(_, clinic_id: int, doctor_id: int):
    try:
        schedule = interface.get_schedules(doctor_id, clinic_id=clinic_id)
    except errors.NoDoctorFoundError as error:
        raise NotFound(error)

    serializer = serializers.DoctorScheduleSerializer(schedule, many=True)
    return Response(serializer.data)


@csrf_exempt
def add_schedule(request: HttpRequest, clinic_id: int, doctor_id: int):
    data = json.loads(request.body)

    serializer = serializers.AddressSerializer(data=data['office_address'])
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    data['clinic_id'] = clinic_id
    data['doctor_id'] = doctor_id

    serializer = serializers.DoctorScheduleSerializer(data=data)
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    data['clinic_id'] = interface.get_clinic(clinic_id)
    data['doctor_id'] = interface.get_doctor(doctor_id)

    schedule = interface.add_schedule(**data)
    serializer = serializers.DoctorScheduleSerializer(schedule, many=False)
    return HttpResponse(serializer.data)


@csrf_exempt
def update_schedule(request: HttpRequest, clinic_id: int, doctor_id: int, schedule_id: int):
    data = json.loads(request.body)

    schedule = interface.get_schedule(schedule_id)
    serializer = serializers.AddressSerializer(schedule.office_address, data=data['office_address'])
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    data['clinic_id'] = clinic_id
    data['doctor_id'] = doctor_id

    serializer = serializers.DoctorScheduleSerializer(schedule, data=data)
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    data['clinic_id'] = interface.get_clinic(clinic_id)
    data['doctor_id'] = interface.get_doctor(doctor_id)

    schedule = interface.update_schedule(schedule_id, **data)
    serializer = serializers.DoctorScheduleSerializer(schedule, many=False)
    return HttpResponse(serializer.data)


@api_view(['DELETE'])
def remove_schedule(_, **kwargs):
    interface.remove_schedule(kwargs['schedule_id'])
    return Response()


@api_view(['GET'])
def get_clinic_doctor_appointment_slots(_, clinic_id: int, doctor_id: int, schedule_date: datetime.date):
    slots = interface.get_appointment_slots(doctor_id, clinic_id, schedule_date)
    serializer = serializers.DoctorAppointmentSlotSerializer(slots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_clinic_patients(_, clinic_id: int):
    try:
        patients = interface.get_patients(clinic_id=clinic_id)
    except errors.NoClinicFoundError as error:
        raise NotFound(error)

    serializer = serializers.PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctors(_):
    doctors = interface.get_doctors()
    serializer = serializers.DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctor(_, doctor_id: int):
    doctor = interface.get_doctor(doctor_id)
    serializer = serializers.DoctorSerializer(doctor)
    return Response(serializer.data)


@csrf_exempt
def add_doctor(request: HttpRequest):
    data = json.loads(request.body)

    serializer = serializers.DoctorSerializer(data=data)
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    if 'specialties' not in data or not isinstance(data['specialties'], list) or not data['specialties']:
        return HttpResponseBadRequest()

    doctor = interface.add_doctor(**data)
    serializer = serializers.DoctorSerializer(doctor, many=False)
    return HttpResponse(serializer.data)


@csrf_exempt
def update_doctor(request: HttpRequest, doctor_id: int) -> HttpResponse:
    data = json.loads(request.body)

    doctor = interface.get_doctor(doctor_id)
    serializer = serializers.DoctorSerializer(doctor, data=data)
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    if 'specialties' not in data or not isinstance(data['specialties'], list) or not data['specialties']:
        return HttpResponseBadRequest()
    
    doctor = interface.update_doctor(doctor_id, **data)
    serializer = serializers.DoctorSerializer(doctor, many=False)
    return HttpResponse(serializer.data)   


@api_view(['GET'])
def get_doctor_specialties(_, doctor_id: int):
    try:
        specialties = interface.get_doctor_specialties(doctor_id)
    except errors.NoDoctorFoundError as error:
        raise NotFound(error)

    serializer = serializers.ProcedureSerializer(specialties, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctor_clinics(_, doctor_id: int):
    try:
        clinics = interface.get_clinics(doctor_id=doctor_id)
    except errors.NoDoctorFoundError as error:
        raise NotFound(error)

    serializer = serializers.ClinicSerializer(clinics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctor_patients(_, doctor_id: int):
    try:
        patients = interface.get_patients(doctor_id=doctor_id)
    except errors.NoDoctorFoundError as error:
        raise NotFound(error)

    serializer = serializers.PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctor_schedules(_, doctor_id: int):
    try:
        schedules = interface.get_schedules(doctor_id)
    except errors.NoDoctorFoundError as error:
        raise NotFound(error)
    
    serializer = serializers.DoctorScheduleSerializer(schedules, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_patients(_):
    patients = interface.get_patients()
    serializer = serializers.PatientSerializer(patients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_patient(_, patient_id: int):
    patient = interface.get_patient(patient_id)
    serializer = serializers.PatientSerializer(patient)
    return Response(serializer.data)


@csrf_exempt
def add_patient(request: HttpRequest) -> HttpResponse:
    data = json.loads(request.body)

    serializer = serializers.PatientSerializer(data=data)
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    serializer = serializers.AddressSerializer(data=data['address'])
    if not serializer.is_valid():
        return HttpResponseBadRequest()

    patient = interface.add_patient(**data)
    serializer = serializers.PatientSerializer(patient, many=False)
    return HttpResponse(serializer.data)


@csrf_exempt
def update_patient(request: HttpRequest, patient_id: int) -> HttpResponse:
    data = json.loads(request.body)

    patient = interface.get_patient(patient_id)
    serializer = serializers.PatientSerializer(patient, data=data)
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    serializer = serializers.AddressSerializer(patient.address, data=data['address'])
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    patient = interface.update_patient(patient_id, **data)
    serializer = serializers.PatientSerializer(patient, many=False)
    return HttpResponse(serializer.data)


@api_view(['GET'])
def get_patient_appointments(_, patient_id: int):
    try:
        appointments = interface.get_patient_appointments(patient_id)
    except errors.NoPatientFoundError as error:
        raise NotFound(error)
    
    serializer = serializers.AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_patient_last_appointments(_, patient_id: int):
    try:
        appointments = interface.get_patient_appointments(patient_id, interface.PatientAppointmentMode.LAST)
    except errors.NoPatientFoundError as error:
        raise NotFound(error)
    
    serializer = serializers.AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_patient_next_appointments(_, patient_id: int):
    try:
        appointments = interface.get_patient_appointments(patient_id, interface.PatientAppointmentMode.NEXT)
    except errors.NoPatientFoundError as error:
        raise NotFound(error)
    
    serializer = serializers.AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@csrf_exempt
def add_patient_appointment(request: HttpRequest, patient_id: int):
    data = json.loads(request.body)
    data['patient_id'] = patient_id

    serializer = serializers.AppointmentSerializer(data=data)
    if not serializer.is_valid():
        return HttpResponseBadRequest()
    
    data['patient_id'] = interface.get_patient(patient_id)
    data['procedure_id'] = interface.get_procedure(data['procedure_id'])
    data['clinic_id'] = interface.get_clinic(data['clinic_id'])
    data['doctor_id'] = interface.get_doctor(data['doctor_id'])

    appointment = interface.add_appointment(**data)
    serializer = serializers.AppointmentSerializer(appointment, many=False)
    return HttpResponse(serializer.data)


@api_view(['GET'])
def get_procedures(_):
    serializer = serializers.ProcedureSerializer(interface.get_procedures(), many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_procedure_clinics(_, procedure_id: int):
    clinics = interface.get_clinics(procedure_id=procedure_id)
    serializer = serializers.ClinicSerializer(clinics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_procedure_clinic_doctors(_, procedure_id: int, clinic_id: int):
    doctors = interface.get_doctors(procedure_id=procedure_id, clinic_id=clinic_id)
    serializer = serializers.DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_appointment_procedures(_, appointment_id: int):
    procedures = interface.get_procedures(appointment_id)
    serializer = serializers.ProcedureSerializer(procedures, many=True)
    return Response(serializer.data)
