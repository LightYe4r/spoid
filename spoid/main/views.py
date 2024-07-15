from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .serializers import *
from datetime import datetime, timedelta
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

period = 7

table_serializers = {
    'CPU': CpuDataSerializer,
    'GPU': GpuDataSerializer,
    'MEMORY': MemoryDataSerializer,
    'MAINBOARD': MainboardDataSerializer,
    'POWER': PowerDataSerializer,
    'STORAGE': StorageDataSerializer,
    'PcCase': PcCaseDataSerializer,
    'COOLER': CoolerDataSerializer,
}

table_price_serializers = {
    'CPU': CpuPriceDataSerializer,
    'GPU': GpuPriceDataSerializer,
    'MEMORY': MemoryPriceDataSerializer,
    'MAINBOARD': MainboardPriceDataSerializer,
    'POWER': PowerPriceDataSerializer,
    'STORAGE': StoragePriceDataSerializer,
    'PcCase': PcCasePriceDataSerializer,
    'COOLER': CoolerPriceDataSerializer,
}


def dictfetchall(cursor):
    "Return all rows from a cursor as a dictionary"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# # 원하는 테이블들의 데이터를 최신순으로 10개씩 가져오고 해당 데이터들의 pk로 price테이블의 componentid를 매핑해서 pagenation하는 API
# class GetTableData(APIView):
#     def post(self, request):
#         table_names = request.data['table_names']
#         table_pages = request.data['table_pages']
#         date_filter = '2024-06-01'
#         data = {}
#         for table_name in table_names:
#             cursor = connection.cursor()
#             cursor.execute(f"""
#                 SELECT {table_name}.*, 
#                        GROUP_CONCAT(Price.Date) as Date,
#                        GROUP_CONCAT(Price.Shop) as Shop,
#                        GROUP_CONCAT(Price.Price) as Price,
#                        GROUP_CONCAT(Price.URL) as URL
#                 FROM {table_name}
#                 JOIN Price ON {table_name}.ComponentID = Price.ComponentID
#                 WHERE Price.Date = %s
#                 GROUP BY {table_name}.ComponentID, {table_name}.Type
#                 LIMIT %s OFFSET %s
#             """, [date_filter, (table_pages[table_name]+1)*10, (table_pages[table_name]+1)*10-10])
#             sql_data = dictfetchall(cursor)
#             for item in sql_data:
#                 item['Date'] = item['Date'].split(',') if item['Date'] else []
#                 item['Shop'] = item['Shop'].split(',') if item['Shop'] else []
#                 item['Price'] = item['Price'].split(',') if item['Price'] else []
#                 item['URL'] = item['URL'].split(',') if item['URL'] else []
#                 item['LowestPrice'] = min([int(price) for price in item['Price'] if price])
#                 item['LowestShop'] = item['Shop'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
#                 item['LowestURL'] = item['URL'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
#             # 쿼리 데이터를 직렬화
#             serializer = table_price_serializers[table_name](sql_data, many=True)
#             data[table_name] = serializer.data
        
#         return Response(data, status=status.HTTP_200_OK)
    
class ComponentDetail(APIView):
    def post(self, request):
        data = request.data
        component_id = data['component_id']
        component_type = data['component_type']
        component_table = component_type
        # component_type = component_type.upper()
        if component_type == 'CASE':
            component_table = 'PcCase'
        cursor = connection.cursor()
        query = f"""
                SELECT c.*, 
                GROUP_CONCAT(pr.Date) as Date,
                GROUP_CONCAT(pr.Shop) as Shop,
                GROUP_CONCAT(pr.Price) as Price,
                GROUP_CONCAT(pr.URL) as URL,
                CAST(ROUND(IFNULL(AVG(last_45_days.Price), 0)) AS UNSIGNED) AS AvgPriceLast45Days
            FROM {component_table} c
            JOIN (
                SELECT pr1.ComponentID, pr1.Shop, pr1.Date, pr1.Price, pr1.URL
                FROM Price pr1
                JOIN (
                    SELECT ComponentID, Shop, MAX(Date) as MaxDate
                    FROM Price
                    WHERE ComponentID = '{component_id}'
                    GROUP BY ComponentID, Shop
                ) pr2
                ON pr1.ComponentID = pr2.ComponentID AND pr1.Shop = pr2.Shop AND pr1.Date = pr2.MaxDate
            ) pr
            ON c.ComponentID = pr.ComponentID
            LEFT JOIN (
                SELECT ComponentID, ROUND(AVG(Price)) AS Price
                FROM (
                    SELECT ComponentID, Date, MIN(Price) AS Price
                    FROM Price
                    WHERE Date >= DATE_SUB(CURDATE(), INTERVAL {period} DAY)
                    GROUP BY ComponentID, Date
                ) daily_min_prices
                GROUP BY ComponentID
            ) last_45_days
            ON c.ComponentID = last_45_days.ComponentID
            WHERE c.ComponentID = '{component_id}'
            GROUP BY c.ComponentID, c.Type;

        """
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 후처리하여 리스트로 변환
        for item in sql_data:
            item['Date'] = item['Date'].split(',') if item['Date'] else []
            item['Shop'] = item['Shop'].split(',') if item['Shop'] else []
            item['Price'] = item['Price'].split(',') if item['Price'] else []
            item['URL'] = item['URL'].split(',') if item['URL'] else []
            try:
                item['LowestPrice'] = min([int(price) for price in item['Price'] if price !=0])
            except:
                item['LowestPrice'] = 0
            item['LowestShop'] = item['Shop'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else 0
            item['LowestURL'] = item['URL'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else 0

        query = f"""
                    WITH daily_min_prices AS (
                        SELECT ComponentID, Type, Date, MIN(Price) AS MinPrice
                        FROM Price
                        WHERE ComponentID = '{component_id}' AND Date >= DATE_SUB(CURDATE(), INTERVAL {period} DAY)
                        GROUP BY ComponentID, Type, Date
                    ),
                    daily_prices_with_shop AS (
                        SELECT p.ComponentID, p.Type, p.Date, p.Price AS MinPrice, p.Shop
                        FROM Price p
                        INNER JOIN daily_min_prices dmp ON p.ComponentID = dmp.ComponentID AND p.Type = dmp.Type AND p.Date = dmp.Date AND p.Price = dmp.MinPrice
                    )
                    SELECT
                        dpws.ComponentID,
                        dpws.Type,
                        MAX(CASE WHEN dpws.Date = '{datetime.today().strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day1,
                        MAX(CASE WHEN dpws.Date = '{datetime.today().strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day1shop,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day2,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day2shop,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day3,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day3shop,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day4,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day4shop,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day5,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day5shop,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day6,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day6shop,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=6)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day7,
                        MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=6)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day7shop
                    FROM daily_prices_with_shop dpws
                    GROUP BY dpws.ComponentID, dpws.Type;
        """
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)
        price_data = dictfetchall(cursor)
        for item in price_data:
            item['day1'] = item['day1'] if item['day1'] else 0
            item['day2'] = item['day2'] if item['day2'] else 0
            item['day3'] = item['day3'] if item['day3'] else 0
            item['day4'] = item['day4'] if item['day4'] else 0
            item['day5'] = item['day5'] if item['day5'] else 0
            item['day6'] = item['day6'] if item['day6'] else 0
            item['day7'] = item['day7'] if item['day7'] else 0
            item['Price'] = [item['day7'], item['day6'], item['day5'], item['day4'], item['day3'], item['day2'], item['day1']]

        # 쿼리 데이터를 직렬화
        component_serializer = table_price_serializers[component_type](sql_data, many=True)
        price_serializer = Price45DaysSerializer(price_data, many=True)

        response_data = {
            "component_data": component_serializer.data,
            "price_data": price_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
class CreateOrder(APIView):
    def post(self, request):
        data = request.data
        order_id = f"{datetime.now().isoformat()}+{data['user_id']}"
        cursor = connection.cursor()
        query = f"""
                        INSERT INTO Orders (OrderID, UserID, CPUID, CpuType, GPUID, GpuType, MemoryID, MemoryType,
                         CoolerID, CoolerType, MainboardID, MainboardType, StorageID, StorageType, PcCaseID, PcCaseType,
                         PowerID, PowerType) VALUES ('{order_id}', '{data['user_id']}', '{data['cpu_id']}',
                         'CPU', '{data['gpu_id']}', 'GPU', '{data['memory_id']}', 'MEMORY',
                         '{data['cooler_id']}', 'COOLER', '{data['mainboard_id']}', 'MAINBOARD',
                         '{data['storage_id']}', 'STORAGE', '{data['pc_case_id']}', 'CASE', 
                         '{data['power_id']}', 'POWER')"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)
        # cursor.execute(f"""INSERT INTO Orders (OrderID, UserID, CPUID, CpuType, GPUID, GpuType, MemoryID, MemoryType,
        #                 CoolerID, CoolerType, MainboardID, MainboardType, StorageID, StorageType, PcCaseID, PcCaseType,
        #                 PowerID, PowerType) VALUES ('{order_id}', '{data['user_id']}', '{data['cpu_id']}',
        #                 'CPU', '{data['gpu_id']}', 'GPU', '{data['memory_id']}', 'MEMORY',
        #                 '{data['cooler_id']}', 'COOLER', '{data['mainboard_id']}', 'MAINBOARD',
        #                 '{data['storage_id']}', 'STORAGE', '{data['pc_case_id']}', 'CASE', 
        #                 '{data['power_id']}', 'POWER')""")
        query = f"""
                SELECT * FROM Orders WHERE orderID = '{order_id}'
                """
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)
        # cursor.execute(f"""SELECT * FROM Orders WHERE OrderID = '{order_id}'""")
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = OrdersDataSerializer(sql_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DetailOrder(APIView):
    def post(self, request):
        data = request.data
        cursor = connection.cursor()
        query = f"""SELECT * FROM Orders WHERE OrderID = '{data['order_id']}'"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = OrdersDataSerializer(sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetOrder(APIView):
    def post(self, request):
        data = request.data
        cursor = connection.cursor()
        query = f"""SELECT * FROM Orders WHERE UserID = '{data['user_id']}'"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)
        if cursor.rowcount == 0:
            return Response([], status=status.HTTP_200_OK)
        query = f"""select Orders.OrderID, User.UserID, CPU.Model AS 'CPU', PcCase.Model AS 'PcCase', GPU.Model AS 'GPU', MEMORY.Model AS 'MEMORY', STORAGE.Model AS 'STORAGE', COOLER.Model AS 'COOLER', MAINBOARD.Model AS 'MAINBOARD', POWER.Model AS 'POWER', PcCase.ImageURL AS 'ImageURL'  
                        from Orders
                        INNER Join User on User.UserID = Orders.UserID
                        INNER Join CPU on CPU.ComponentID = Orders.CPUID
                        INNER Join GPU on GPU.ComponentID = Orders.GPUID
                        INNER Join MEMORY on MEMORY.ComponentID = Orders.MemoryID
                        INNER Join STORAGE on STORAGE.ComponentID = Orders.StorageID
                        INNER Join MAINBOARD on MAINBOARD.ComponentID = Orders.MainboardID
                        INNER Join PcCase on PcCase.ComponentID = Orders.PcCaseID
                        INNER Join COOLER on COOLER.ComponentID = Orders.CoolerID
                        INNER Join POWER on POWER.ComponentID = Orders.PowerID
                        WHERE Orders.UserID = '{data['user_id']}'"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)
        sql_data = dictfetchall(cursor)
        
        query = f"""
                SELECT o.OrderID, CAST(SUM(p.MinPrice) as unsigned) AS TotalPrice
                FROM Orders o
                LEFT JOIN (
                    SELECT p.ComponentID, MIN(p.Price) AS MinPrice
                    FROM Price p
                    JOIN (
                        SELECT ComponentID, MAX(Date) AS MaxDate
                        FROM Price
                        GROUP BY ComponentID
                    ) latest ON p.ComponentID = latest.ComponentID AND p.Date = latest.MaxDate
                    GROUP BY p.ComponentID
                ) p ON p.ComponentID IN (
                    o.CPUID, 
                    o.GPUID, 
                    o.MemoryID, 
                    o.StorageID, 
                    o.MainboardID, 
                    o.PcCaseID, 
                    o.CoolerID, 
                    o.PowerID
                )
                WHERE o.UserID = '{data['user_id']}'
                Group BY o.OrderID;
        """
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor)
        total_price = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = OrderListviewSerializer(sql_data, many=True)
        i = 0
        print(total_price)
        for item in serializer.data:
            print(total_price[i]['TotalPrice'])
            item['TotalPrice'] = total_price[i]['TotalPrice']
            print(item['TotalPrice'])
            i += 1
        print(item)
        ResponseData = {
            "order_data": serializer.data
        }

        return Response(ResponseData, status=status.HTTP_200_OK)

class CreateUser(APIView):
    def post(self, request):
        data = request.data
        cursor = connection.cursor()
        query = f"""INSERT INTO User (UserID, Name, Email) VALUES ('{data['user_id']}', '{data['user_name']}', '{data['user_email']}')"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)

        query = f"""SELECT * FROM User WHERE UserID = '{data['user_id']}'"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)
        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화

        serializer = UserDataSerializer(sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateFavorite(APIView):
    def post(self, request):
        data = request.data
        # data['component_type'] = data['component_type'].upper()
        # if data['component_type'] == 'CASE' or data['component_type'] == 'PCCASE':
        #     data['component_type'] = 'CASE'
        favorite_id = f"{datetime.now().isoformat()}+{data['user_id']}"
        cursor = connection.cursor()
        query = f"""INSERT INTO Favorite (FavoriteID, UserID, ComponentID, Type) VALUES ('{favorite_id}', '{data['user_id']}', '{data['component_id']}', '{data['component_type']}')"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)

        query = f"""SELECT * FROM Favorite WHERE UserID = '{data['user_id']}'"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)

        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = FavoriteDataSerializer(sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DeleteFavorite(APIView):
    def post(self, request):
        data = request.data
        # data['component_type'] = data['component_type'].upper()
        # if data['component_type'] == 'CASE':
        #     data['component_type'] = 'PcCase'
        cursor = connection.cursor()
        query = f"""DELETE FROM Favorite WHERE UserID = '{data['user_id']}' AND ComponentID = '{data['component_id']}' AND Type = '{data['component_type']}'"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)

        query =f"""SELECT * FROM Favorite WHERE UserID = '{data['user_id']}'"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)

        sql_data = dictfetchall(cursor)
        # 쿼리 데이터를 직렬화
        serializer = FavoriteDataSerializer(sql_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetComponentListWithFavorite(APIView):
    def post(self, request):
        data = request.data
        table_name = data['component_type']
        table_type = table_name
        cursor = connection.cursor()
        # table_name = table_name.upper()
        if table_name == 'CASE' or table_name == 'PcCase':
            table_name = 'PcCase'
            table_type = 'CASE'

        # 컴포넌트 ID 목록 조회
        query = f"""SELECT ComponentID FROM Price WHERE Type = '{table_type}'"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)


        sql_data = dictfetchall(cursor)
        sql_data = [item['ComponentID'] for item in sql_data]
        logger.info(sql_data)
        sql_data = list(set(sql_data))
        component_ids_str = ','.join([f"'{item}'" for item in sql_data])
        
        if not component_ids_str:
            return Response([], status=status.HTTP_200_OK)
        # 최신 데이터를 가져오는 쿼리
        query = f"""
            SELECT  c.*, 
                    GROUP_CONCAT(p.Date) as Date,
                    GROUP_CONCAT(p.Shop) as Shop,
                    GROUP_CONCAT(p.Price) as Price,
                    GROUP_CONCAT(p.URL) as URL,
                    CAST(ROUND(IFNULL(AVG(last_45_days.Price), 0)) AS UNSIGNED) AS AvgPriceLast45Days
            FROM {table_name} c
            JOIN (
                SELECT p1.ComponentID, p1.Shop, p1.Date, p1.Price, p1.URL
                FROM Price p1
                JOIN (
                    SELECT ComponentID, Shop, MAX(Date) as MaxDate
                    FROM Price
                    WHERE ComponentID IN ({component_ids_str})
                    GROUP BY ComponentID, Shop
                ) p2
                ON p1.ComponentID = p2.ComponentID AND p1.Shop = p2.Shop AND p1.Date = p2.MaxDate
            ) p
            ON c.ComponentID = p.ComponentID
            LEFT JOIN (
                SELECT ComponentID, ROUND(AVG(Price)) AS Price
                FROM (
                    SELECT ComponentID, Date, MIN(Price) AS Price
                    FROM Price
                    WHERE Date >= DATE_SUB(CURDATE(), INTERVAL {period} DAY)
                    GROUP BY ComponentID, Date
                ) daily_min_prices
                GROUP BY ComponentID
            ) last_45_days
            ON c.ComponentID = last_45_days.ComponentID
            WHERE c.ComponentID IN ({component_ids_str})
            GROUP BY c.ComponentID, c.Type
        """
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)
        sql_data = dictfetchall(cursor)
        
        for item in sql_data:
            item['Date'] = item['Date'].split(',') if item['Date'] else []
            item['Shop'] = item['Shop'].split(',') if item['Shop'] else []
            item['Price'] = item['Price'].split(',') if item['Price'] else []
            item['URL'] = item['URL'].split(',') if item['URL'] else []
            if item['Price']:
                try:
                    item['LowestPrice'] = min([int(price) for price in item['Price'] if price != 0])
                except:
                    item['LowestPrice'] = 0
                item['LowestShop'] = item['Shop'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else 0
                item['LowestURL'] = item['URL'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else 0
            else:
                item['LowestPrice'] = 0
                item['LowestShop'] = 0
                item['LowestURL'] = 0
        
        # 쿼리 데이터를 직렬화
        if table_name == 'PcCase':
            serializer = table_price_serializers['PcCase'](sql_data, many=True)
        else:    
            serializer = table_price_serializers[data['component_type']](sql_data, many=True)
        
        if data['user_id'] == 'None':
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        query = f"""SELECT * FROM Favorite WHERE UserID = '{data['user_id']}'"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)

        favorite_data = dictfetchall(cursor)
        favorite_data = [item['ComponentID'] for item in favorite_data]
        
        for item in serializer.data:
            item['IsFavorite'] = item['ComponentID'] in favorite_data
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetFavoriteListWithComponent(APIView):
    def post(self, request):
        data = request.data
        user_id = data['user_id']
        
        cursor = connection.cursor()
        query = f"""SELECT ComponentID, Type FROM Favorite WHERE UserID = '{user_id}'"""
        logger.info(query)
        cursor.execute(query)
        logger.info(cursor.description)
        favorite_data = dictfetchall(cursor)
        type_component_map = {}
        for component in favorite_data:
            component_type = component['Type']
            component_table = component_type
            # component_type = component_type.upper()
            if component_type not in type_component_map:
                type_component_map[component_type] = []
            type_component_map[component_type].append(component['ComponentID'])
        
        query_data = {}
        for component_type, component_ids in type_component_map.items():
            component_table = component_type
            if component_type == 'CASE':
                component_table = 'PcCase'
            component_ids_str = ",".join([f"'{item}'" for item in component_ids])
            query = f"""
                SELECT c.*, 
                    GROUP_CONCAT(p.Date) AS Date,
                    GROUP_CONCAT(p.Shop) AS Shop,
                    GROUP_CONCAT(p.Price) AS Price,
                    GROUP_CONCAT(p.URL) AS URL,
                    CAST(ROUND(IFNULL(AVG(last_45_days.Price), 0)) AS UNSIGNED) AS AvgPriceLast45Days
                FROM {component_table} c
                JOIN (
                    SELECT p1.ComponentID, p1.Shop, p1.Date, p1.Price, p1.URL
                    FROM Price p1
                    JOIN (
                        SELECT ComponentID, Shop, MAX(Date) AS MaxDate
                        FROM Price
                        WHERE ComponentID IN ({component_ids_str})
                        GROUP BY ComponentID, Shop
                    ) p2
                    ON p1.ComponentID = p2.ComponentID AND p1.Shop = p2.Shop AND p1.Date = p2.MaxDate
                ) p
                ON c.ComponentID = p.ComponentID
                LEFT JOIN (
                    SELECT ComponentID, AVG(Price) AS Price
                    FROM (
                        SELECT ComponentID, Date, MIN(Price) AS Price
                        FROM Price
                        WHERE Date >= DATE_SUB(CURDATE(), INTERVAL {period} DAY)
                        GROUP BY ComponentID, Date
                    ) daily_min_prices
                    GROUP BY ComponentID
                ) last_45_days
                ON c.ComponentID = last_45_days.ComponentID
                WHERE c.ComponentID IN ({component_ids_str})
                GROUP BY c.ComponentID, c.Type;
            """
            logger.info(query)
            cursor.execute(query)
            logger.info(cursor.description)
            sql_data = dictfetchall(cursor)
            for item in sql_data:
                item['Date'] = item['Date'].split(',') if item['Date'] else []
                item['Shop'] = item['Shop'].split(',') if item['Shop'] else []
                item['Price'] = item['Price'].split(',') if item['Price'] else []
                item['URL'] = item['URL'].split(',') if item['URL'] else []
                if item['Price']:
                    try:
                        item['LowestPrice'] = min([int(price) for price in item['Price'] if price != 0])
                    except:
                        item['LowestPrice'] = 0
                    item['LowestShop'] = item['Shop'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else 0
                    item['LowestURL'] = item['URL'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else 0
                else:
                    item['LowestPrice'] = 0
                    item['LowestShop'] = 0
                    item['LowestURL'] = 0
            # 쿼리 데이터를 직렬화
            serializer = table_price_serializers[component_type](sql_data, many=True)
            query_data[component_type] = serializer.data

        return Response(query_data, status=status.HTTP_200_OK)
    
class GetLandingPage(APIView):
    def post(self, request):
        # 부품별 랜덤 데이터의 정보와, 그 데이터의 최저가 정보 그 shop, 최근 7일간의 가격들을 가져오는 쿼리
        cursor = connection.cursor()
        components = ['CPU', 'GPU', 'MEMORY', 'MAINBOARD', 'POWER', 'STORAGE', 'PcCase', 'COOLER']
        query_data = {}
        for component in components:
            query = f"""
            WITH random_component AS (
                SELECT *
                FROM {component}
                ORDER BY RAND()
                LIMIT 1
            )
            SELECT 
                c.*, 
                GROUP_CONCAT(p.Date) AS Date,
                GROUP_CONCAT(p.Shop) AS Shop,
                GROUP_CONCAT(p.Price) AS Price,
                GROUP_CONCAT(p.URL) AS URL,
                CAST(ROUND(IFNULL(last_45_days.AvgPrice, 0)) AS UNSIGNED) AS AvgPriceLast45Days
            FROM 
                random_component c
            JOIN (
                SELECT 
                    p1.ComponentID, 
                    p1.Shop, 
                    p1.Date, 
                    p1.Price, 
                    p1.URL
                FROM 
                    Price p1
                JOIN (
                    SELECT 
                        ComponentID, 
                        Shop, 
                        MAX(Date) AS MaxDate
                    FROM 
                        Price
                    WHERE 
                        ComponentID IN (SELECT ComponentID FROM random_component)
                    GROUP BY 
                        ComponentID, Shop
                ) p2 ON 
                    p1.ComponentID = p2.ComponentID AND 
                    p1.Shop = p2.Shop AND 
                    p1.Date = p2.MaxDate
            ) p ON 
                c.ComponentID = p.ComponentID
            LEFT JOIN (
                SELECT 
                    ComponentID, 
                    ROUND(AVG(Price)) AS AvgPrice
                FROM (
                    SELECT 
                        ComponentID, 
                        Date, 
                        MIN(Price) AS Price
                    FROM 
                        Price
                    WHERE 
                        Date >= DATE_SUB(CURDATE(), INTERVAL {period} DAY)
                    GROUP BY 
                        ComponentID, Date
                ) daily_min_prices
                GROUP BY 
                    ComponentID
            ) last_45_days ON 
                c.ComponentID = last_45_days.ComponentID
            GROUP BY 
                c.ComponentID, 
                c.Type;
                    """
            logger.info(query)
            cursor.execute(query)
            logger.info(cursor.description)
            sql_data = dictfetchall(cursor)
            for item in sql_data:
                item['Date'] = item['Date'].split(',') if item['Date'] else []
                item['Shop'] = item['Shop'].split(',') if item['Shop'] else []
                item['Price'] = item['Price'].split(',') if item['Price'] else []
                item['URL'] = item['URL'].split(',') if item['URL'] else []
                try:
                    item['LowestPrice'] = min([int(price) for price in item['Price'] if price !=0])
                except:
                    item['LowestPrice'] = 0    
                item['LowestShop'] = item['Shop'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None
                item['LowestURL'] = item['URL'][item['Price'].index(str(item['LowestPrice']))] if item['LowestPrice'] else None

            # 쿼리 데이터를 직렬화
            serializer = table_price_serializers[component](sql_data, many=True)
            query_data[component] = serializer.data
            print(query_data)
            # component_id = query_data[component][0]['ComponentID']
            component_id = 'C1'
            query = f"""
                        WITH daily_min_prices AS (
                            SELECT ComponentID, Type, Date, MIN(Price) AS MinPrice
                            FROM Price
                            WHERE ComponentID = '{component_id}' AND Date >= DATE_SUB(CURDATE(), INTERVAL {period} DAY)
                            GROUP BY ComponentID, Type, Date
                        ),
                        daily_prices_with_shop AS (
                            SELECT p.ComponentID, p.Type, p.Date, p.Price AS MinPrice, p.Shop
                            FROM Price p
                            INNER JOIN daily_min_prices dmp ON p.ComponentID = dmp.ComponentID AND p.Type = dmp.Type AND p.Date = dmp.Date AND p.Price = dmp.MinPrice
                        )
                        SELECT
                            dpws.ComponentID,
                            dpws.Type,
                            MAX(CASE WHEN dpws.Date = '{datetime.today().strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day1,
                            MAX(CASE WHEN dpws.Date = '{datetime.today().strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day1shop,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day2,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day2shop,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day3,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day3shop,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day4,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day4shop,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day5,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day5shop,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day6,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day6shop,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=6)).strftime('%Y-%m-%d')}' THEN dpws.MinPrice END) AS day7,
                            MAX(CASE WHEN dpws.Date = '{(datetime.today() - timedelta(days=6)).strftime('%Y-%m-%d')}' THEN dpws.Shop END) AS day7shop
                        FROM daily_prices_with_shop dpws
                        GROUP BY dpws.ComponentID, dpws.Type;
            """
            logger.info(query)
            cursor.execute(query)
            logger.info(cursor.description)

            price_data = dictfetchall(cursor)
            for item in price_data:
                item['day1'] = item['day1'] if item['day1'] else 0
                item['day2'] = item['day2'] if item['day2'] else 0
                item['day3'] = item['day3'] if item['day3'] else 0
                item['day4'] = item['day4'] if item['day4'] else 0
                item['day5'] = item['day5'] if item['day5'] else 0
                item['day6'] = item['day6'] if item['day6'] else 0
                item['day7'] = item['day7'] if item['day7'] else 0
                item['Price'] = [item['day7'], item['day6'], item['day5'], item['day4'], item['day3'], item['day2'], item['day1']]

            # 쿼리 데이터를 직렬화
            price_serializer = Price45DaysSerializer(price_data, many=True)
            query_data[component + '_price'] = price_serializer.data

        return Response(query_data, status=status.HTTP_200_OK)