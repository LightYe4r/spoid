from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .serializers import *
from datetime import datetime

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


def dictfetchall(cursor):
    "Return all rows from a cursor as a dictionary"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# 원하는 테이블들의 데이터를 최신순으로 10개씩 가져오고 해당 데이터들의 pk로 price테이블의 componentid를 매핑해서 pagenation하는 API
class GetTableData(APIView):
    def post(self, request):
        table_names = request.data['table_names']
        table_pages = request.data['table_pages']
        date_filter = '2024-06-01'
        data = {}
        for table_name in table_names:
            cursor = connection.cursor()
            cursor.execute(f"""
                SELECT {table_name}.*, 
                       GROUP_CONCAT(Price.Date) as Dates,
                       GROUP_CONCAT(Price.Shop) as Shops,
                       GROUP_CONCAT(Price.Price) as Prices,
                       GROUP_CONCAT(Price.URL) as URLs
                FROM {table_name}
                JOIN Price ON {table_name}.ComponentID = Price.ComponentID
                WHERE Price.Date = %s
                GROUP BY {table_name}.ComponentID, {table_name}.Type
                LIMIT %s OFFSET %s
            """, [date_filter, (table_pages[table_name]+1)*10, (table_pages[table_name]+1)*10-10])
            sql_data = dictfetchall(cursor)
            for item in sql_data:
                item['Dates'] = item['Dates'].split(',') if item['Dates'] else []
                item['Shops'] = item['Shops'].split(',') if item['Shops'] else []
                item['Prices'] = item['Prices'].split(',') if item['Prices'] else []
                item['URLs'] = item['URLs'].split(',') if item['URLs'] else []
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
    
class CreateOrder(APIView):
    def post(self, request):
        data = request.data
        order_id = f"{datetime.now().isoformat()}+{data['user_id']}"
        cursor = connection.cursor()
        cursor.execute(f"""INSERT INTO Orders (OrderID, UserID, CPUID, CpuType, GPUID, GpuType, MemoryID, MemoryType,
                        CoolerID, CoolerType, MainboardID, MainboardType, StorageID, StorageType, PcCaseID, PcCaseType,
                        PowerID, PowerType) VALUES ('{order_id}', '{data['user_id']}', '{data['cpu_id']}',
                        '{data['cpu_type']}', '{data['gpu_id']}', '{data['gpu_type']}', '{data['memory_id']}', '{data['memory_type']}',
                        '{data['cooler_id']}', '{data['cooler_type']}', '{data['mainboard_id']}', '{data['mainboard_type']}',
                        '{data['storage_id']}', '{data['storage_type']}', '{data['pc_case_id']}', '{data['pc_case_type']}', 
                        '{data['power_id']}', '{data['power_type']}')""")
        cursor.execute(f"""SELECT * FROM Orders WHERE OrderID = '{order_id}'""")
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = OrdersDataSerializer(sql_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DetailOrder(APIView):
    def post(self, request):
        data = request.data
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * FROM Orders WHERE OrderID = '{data['order_id']}'""")
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = OrdersDataSerializer(sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetOrder(APIView):
    def post(self, request):
        data = request.data
        cursor = connection.cursor()
        cursor.execute(f"""SELECT * FROM Orders WHERE UserID = '{data['user_id']}'""")
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = OrdersDataSerializer(sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateUser(APIView):
    def post(self, request):
        data = request.data
        cursor = connection.cursor()
        cursor.execute(f"""INSERT INTO User (UserID, Name, Email) VALUES ('{data['user_id']}', '{data['user_name']}', '{data['user_email']}')""")
        cursor.execute(f"""SELECT * FROM User WHERE UserID = '{data['user_id']}'""")
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = UserDataSerializer(sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)