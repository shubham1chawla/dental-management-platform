from rest_framework.response import Response
from rest_framework.decorators import api_view
from service.models import Clinic, Doctor
from .serializers import ClinicSerializer, DoctorSerializer


@api_view(['GET'])
def get_clinics(_):
    clinics = Clinic.objects.all()
    serializer = ClinicSerializer(clinics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_doctors(_):
    doctors = Doctor.objects.all()
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)
