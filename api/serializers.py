from rest_framework import serializers
from service.models import Clinic, Doctor, Procedure

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    specialty = ProcedureSerializer(many=False, read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'
