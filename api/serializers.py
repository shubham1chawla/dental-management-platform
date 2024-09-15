from rest_framework import serializers
from service.models import Address, Clinic, Doctor, Procedure


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ClinicSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False, read_only=True)
    
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
