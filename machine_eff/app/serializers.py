from rest_framework import serializers
from .models import Machine,ProductionLog

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = "__all__"

class ProductionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionLog
        fields = "__all__"

class OeeSerializer(serializers.Serializer):
    machine_name = serializers.CharField(max_length=100)
    machine_serial_no = serializers.CharField(max_length=100)
    oee = serializers.FloatField()