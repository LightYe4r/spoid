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
                       GROUP_CONCAT(Price.Date) as Date,
                       GROUP_CONCAT(Price.Shop) as Shop,
                       GROUP_CONCAT(Price.Price) as Price,
                       GROUP_CONCAT(Price.URL) as URL
                FROM {table_name}
                JOIN Price ON {table_name}.ComponentID = Price.ComponentID
                WHERE Price.Date = %s
                GROUP BY {table_name}.ComponentID, {table_name}.Type
                LIMIT %s OFFSET %s
            """, [date_filter, (table_pages[table_name]+1)*10, (table_pages[table_name]+1)*10-10])
            sql_data = dictfetchall(cursor)
            for item in sql_data:
                item['Date'] = item['Date'].split(',') if item['Date'] else []
                item['Shop'] = item['Shop'].split(',') if item['Shop'] else []
                item['Price'] = item['Price'].split(',') if item['Price'] else []
                item['URL'] = item['URL'].split(',') if item['URL'] else []
                item['LowestPrice'] = min([int(price) for price in item['Price'] if price])
                item['LowestShop'] = item['Shop'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
                item['LowestURL'] = item['URL'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
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
        cursor.execute(f"""
            SELECT {component_type}.*, 
                   GROUP_CONCAT(Price.Date) as Date,
                   GROUP_CONCAT(Price.Shop) as Shop,
                   GROUP_CONCAT(Price.Price) as Price,
                   GROUP_CONCAT(Price.URL) as URL
            FROM {component_type}
            JOIN Price ON {component_type}.ComponentID = Price.ComponentID
            WHERE {component_type}.ComponentID = %s
            GROUP BY {component_type}.ComponentID, {component_type}.Type
        """, [component_id])
        sql_data = dictfetchall(cursor)
        
        # 쿼리 데이터를 후처리하여 리스트로 변환
        for item in sql_data:
            item['Date'] = item['Date'].split(',') if item['Date'] else []
            item['Shop'] = item['Shop'].split(',') if item['Shop'] else []
            item['Price'] = item['Price'].split(',') if item['Price'] else []
            item['URL'] = item['URL'].split(',') if item['URL'] else []
            item['LowestPrice'] = min([int(price) for price in item['Price'] if price])
            item['LowestShop'] = item['Shop'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
            item['LowestURL'] = item['URL'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None

        # 쿼리 데이터를 직렬화
        serializer = table_price_serializers[component_type](sql_data, many=True)
        
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
        cursor.execute(f"""select Orders.OrderID, Cpu.Model AS 'CPU', PcCase.Model AS 'PcCase', Gpu.Model AS 'GPU', Memory.Model AS 'Memory', Storage.Model AS 'Storage', Cooler.Model AS 'Cooler', Mainboard.Model AS 'Mainboard', Power.Model AS 'Power, PcCase.ImageURL AS ImageURL'  
                        from Orders
                        LEFT Join User on '{data['user_id']}' = Orders.UserID
                        LEFT Join Cpu on Cpu.ComponentID = Orders.CPUID
                        LEFT Join Gpu on Gpu.ComponentID = Orders.GPUID
                        LEFT Join Memory on Memory.ComponentID = Orders.MemoryID
                        LEFT Join Storage on Storage.ComponentID = Orders.StorageID
                        LEFT Join Mainboard on Mainboard.ComponentID = Orders.MainboardID
                        LEFT Join PcCase on PcCase.ComponentID = Orders.PcCaseID
                        LEFT Join Cooler on Cooler.ComponentID = Orders.CoolerID
                        LEFT Join Power on Power.ComponentID = Orders.PowerID""")
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = OrderListviewSerializer(sql_data, many=True)
        
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
    
class GetComponentList(APIView):
    def post(self, request):
        data = request.data
        table_name = data['component_type']
        cursor = connection.cursor()
        cursor.execute(f"""
                SELECT {table_name}.*, 
                       GROUP_CONCAT(Price.Date) as Date,
                       GROUP_CONCAT(Price.Shop) as Shop,
                       GROUP_CONCAT(Price.Price) as Price,
                       GROUP_CONCAT(Price.URL) as URL
                FROM {table_name}
                JOIN Price ON {table_name}.ComponentID = Price.ComponentID
                GROUP BY {table_name}.ComponentID, {table_name}.Type
            """)
        sql_data = dictfetchall(cursor)
        for item in sql_data:
            item['Date'] = item['Date'].split(',') if item['Date'] else []
            item['Shop'] = item['Shop'].split(',') if item['Shop'] else []
            item['Price'] = item['Price'].split(',') if item['Price'] else []
            item['URL'] = item['URL'].split(',') if item['URL'] else []
            item['LowestPrice'] = min([int(price) for price in item['Price'] if price])
            item['LowestShop'] = item['Shop'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
            item['LowestURL'] = item['URL'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
        # 쿼리 데이터를 직렬화
        serializer = table_price_serializers[data['component_type']](sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateFavorite(APIView):
    def post(self, request):
        data = request.data
        favorite_id = f"{datetime.now().isoformat()}+{data['user_id']}"
        cursor = connection.cursor()
        cursor.execute(f"""INSERT INTO Favorite (FavoriteID, UserID, ComponentID, Type) VALUES ('{favorite_id}', '{data['user_id']}', '{data['component_id']}', '{data['component_type']}')""")
        cursor.execute(f"""SELECT * FROM Favorite WHERE UserID = '{data['user_id']}'""")
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = FavoriteDataSerializer(sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteFavorite(APIView):
    def post(self, request):
        data = request.data
        cursor = connection.cursor()
        cursor.execute(f"""DELETE FROM Favorite WHERE UserID = '{data['user_id']}' AND ComponentID = '{data['component_id']}' AND Type = '{data['component_type']}'""")
        cursor.execute(f"""SELECT * FROM Favorite WHERE UserID = '{data['user_id']}'""")
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = FavoriteDataSerializer(sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetComponentListWithFavorite(APIView):
    def post(self, request):
        data = request.data
        table_name = data['component_type']
        cursor = connection.cursor()
        cursor.execute(f"""
                SELECT {table_name}.*, 
                       GROUP_CONCAT(Price.Date) as Date,
                       GROUP_CONCAT(Price.Shop) as Shop,
                       GROUP_CONCAT(Price.Price) as Price,
                       GROUP_CONCAT(Price.URL) as URL
                FROM {table_name}
                JOIN Price ON {table_name}.ComponentID = Price.ComponentID
                GROUP BY {table_name}.ComponentID, {table_name}.Type
            """)
        sql_data = dictfetchall(cursor)
        for item in sql_data:
            item['Date'] = item['Date'].split(',') if item['Date'] else []
            item['Shop'] = item['Shop'].split(',') if item['Shop'] else []
            item['Price'] = item['Price'].split(',') if item['Price'] else []
            item['URL'] = item['URL'].split(',') if item['URL'] else []
            item['LowestPrice'] = min([int(price) for price in item['Price'] if price])
            item['LowestShop'] = item['Shop'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
            item['LowestURL'] = item['URL'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
        # 쿼리 데이터를 직렬화
        serializer = table_price_serializers[data['component_type']](sql_data, many=True)
        if data['user_id'] == 'None':
            return Response(serializer.data, status=status.HTTP_200_OK)
        cursor.execute(f"""SELECT * FROM Favorite WHERE UserID = '{data['user_id']}'""")
        favorite_data = dictfetchall(cursor)
        favorite_data = [item['ComponentID'] for item in favorite_data]
        
        for item in serializer.data:
            item['IsFavorite'] = item['ComponentID'] in favorite_data
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetFavoriteListWithComponent(APIView):
    def post(self, requests):
        data = requests.data
        user_id = data['user_id']
        cursor = connection.cursor()
        cursor.execute(f"""SELECT ComponentID, Type FROM Favorite WHERE UserID = '{user_id}'""")
        favorite_data = dictfetchall(cursor)
        type_component_map = {}
        for component_type in favorite_data:
            if component_type['Type'] not in type_component_map:
                type_component_map[component_type['Type']] = []
            type_component_map[component_type['Type']].append(component_type['ComponentID'])
        
        query_data = {}
        for component_type in type_component_map:
            print(f"""
                SELECT {component_type}.*, 
                       GROUP_CONCAT(Price.Date) as Date,
                       GROUP_CONCAT(Price.Shop) as Shop,
                       GROUP_CONCAT(Price.Price) as Price,
                       GROUP_CONCAT(Price.URL) as URL
                FROM {component_type}
                JOIN Price ON {component_type}.ComponentID = Price.ComponentID
                WHERE {component_type}.ComponentID IN ({",".join([f"'{item}'" for item in type_component_map[component_type]])})
                GROUP BY {component_type}.ComponentID, {component_type}.Type
            """)
            cursor.execute(f"""
                SELECT {component_type}.*, 
                       GROUP_CONCAT(Price.Date) as Date,
                       GROUP_CONCAT(Price.Shop) as Shop,
                       GROUP_CONCAT(Price.Price) as Price,
                       GROUP_CONCAT(Price.URL) as URL
                FROM {component_type}
                JOIN Price ON {component_type}.ComponentID = Price.ComponentID
                WHERE {component_type}.ComponentID IN ({",".join([f"'{item}'" for item in type_component_map[component_type]])})
                GROUP BY {component_type}.ComponentID, {component_type}.Type
            """)
            sql_data = dictfetchall(cursor)
            for item in sql_data:
                item['Date'] = item['Date'].split(',') if item['Date'] else []
                item['Shop'] = item['Shop'].split(',') if item['Shop'] else []
                item['Price'] = item['Price'].split(',') if item['Price'] else []
                item['URL'] = item['URL'].split(',') if item['URL'] else []
                item['LowestPrice'] = min([int(price) for price in item['Price'] if price])
                item['LowestShop'] = item['Shop'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
                item['LowestURL'] = item['URL'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
            # 쿼리 데이터를 직렬화
            serializer = table_price_serializers[component_type](sql_data, many=True)
            query_data[component_type] = serializer.data

        return Response(query_data, status=status.HTTP_200_OK)