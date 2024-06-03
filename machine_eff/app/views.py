from rest_framework import generics
from datetime import datetime
import re
from .models import Machine, ProductionLog
from .serializers import MachineSerializer, ProductionLogSerializer, OeeSerializer


class MachineList(generics.ListCreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class MachineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class ProductionLogList(generics.ListCreateAPIView):
    queryset = ProductionLog.objects.all()
    serializer_class = ProductionLogSerializer

class ProductionLogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductionLog.objects.all()
    serializer_class = ProductionLogSerializer

def calculate_oee(machine, start_date, end_date):
    production_logs = ProductionLog.objects.filter(machine=machine, start_time__range=(start_date, end_date))
    available_time = 24  # 3 shifts * 8 hours
    ideal_cycle_time = 5  # minutes
    total_products = 0
    good_products = 0
    bad_products = 0
  
    for log in production_logs:
        total_products += 1
        if log.duration == ideal_cycle_time:
            good_products += 1
        else:
            bad_products += 1
 

    available_operating_time = total_products * ideal_cycle_time
    unplanned_downtime = available_time - available_operating_time
    actual_output = total_products
    quality = (good_products / total_products) * 100
    performance = (ideal_cycle_time * actual_output / available_operating_time) * 100
    availability = ((available_time - unplanned_downtime) / available_time) * 100
    oee = (availability * performance * quality) / 10000

    return oee

class OEEList(generics.ListAPIView):
    serializer_class = OeeSerializer

    def get_queryset(self):
        machines = Machine.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        start = re.findall(r'\d+', start_date)
        end = re.findall(r'\d+', end_date)

        start_date = datetime(int(start[0]),int(start[1]),int(start[2]))
        end_date = datetime(int(end[0]),int(end[1]),int(end[2]))
     
        oee_data = []

        for machine in machines:
            oee = calculate_oee(machine, start_date, end_date)
            print(oee)
            oee_data.append({'machine_name': machine.machine_name,'machine_serial_no': machine.machine_serial_no, 'oee': oee})
        
        return oee_data