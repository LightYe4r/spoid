from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

# 원하는 테이블들의 데이터를 최신순으로 10개씩 가져오고 해당 데이터들의 pk로 price테이블의 componentid를 매핑해서 pagenation하는 API
class GetTableData(APIView):
    def post(self, request):
        table_names = request.data['table_names']
        table_pages = request.data['table_pages']
        data = {}
        for table_name in table_names:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name} join Price on {table_name}.ComponentID = Price.ComponentID LIMIT {(table_pages[table_name]+1)*10} OFFSET {(table_pages[table_name]+1)*10-10}")
            data[table_name] = cursor.fetchall()
        return Response(data, status=status.HTTP_200_OK)