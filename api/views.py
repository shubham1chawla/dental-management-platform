from rest_framework.response import Response
from rest_framework.decorators import api_view
from clinics.models import Clinic
from .serializers import ClinicSerializer

@api_view(['GET'])
def get_clinics(_):
    clinics = Clinic.objects.all()
    serializer = ClinicSerializer(clinics, many=True)
    return Response(serializer.data)