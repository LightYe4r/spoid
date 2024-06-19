from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .serializers import *

table_serializers = {
    'Cpu': CpuDataSerializer,
    'Gpu': GpuDataSerializer,
    'Memory': MemoryDataSerializer,
    'Mainboard': MainboardDataSerializer,
    'Power': PowerDataSerializer,
    'Storage': StorageDataSerializer,
    'PcCase': PcCaseDataSerializer,
    'Cooler': CoolerDataSerializer,
}

table_price_serializers = {
    'Cpu': CpuPriceDataSerializer,
    'Gpu': GpuPriceDataSerializer,
    'Memory': MemoryPriceDataSerializer,
    'Mainboard': MainboardPriceDataSerializer,
    'Power': PowerPriceDataSerializer,
    'Storage': StoragePriceDataSerializer,
    'PcCase': PcCasePriceDataSerializer,
    'Cooler': CoolerPriceDataSerializer,
}

# 원하는 테이블들의 데이터를 최신순으로 10개씩 가져오고 해당 데이터들의 pk로 price테이블의 componentid를 매핑해서 pagenation하는 API
def dictfetchall(cursor):
    "Return all rows from a cursor as a dictionary"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class GetTableData(APIView):
    def post(self, request):
        table_names = request.data['table_names']
        table_pages = request.data['table_pages']
        data = {}
        for table_name in table_names:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name} join Price on {table_name}.ComponentID = Price.ComponentID LIMIT {(table_pages[table_name]+1)*10} OFFSET {(table_pages[table_name]+1)*10-10}")
            sql_data = dictfetchall(cursor)
            print(sql_data)
            # 쿼리 데이터를 직렬화
            serializer = table_price_serializers[table_name](sql_data, many=True)
            data[table_name] = serializer.data
        
        return Response(data, status=status.HTTP_200_OK)
    
class ComponentDetail(APIView):
    def post(self, request):
        data = request.data
        component_id = data['component_id']
        component_type = data['component_type']
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * FROM {component_type} join Price on {component_type}.ComponentID = Price.ComponentID WHERE {component_type}.ComponentID = '{component_id}'""")
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer =  table_price_serializers[component_type](sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)