import boto3
from django.conf import settings
from botocore.exceptions import ClientError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from main.serializers import *

def unicode_to_string(value):
    return value.encode('utf-8').decode('utf-8')

class CreateUser(APIView):
    def get(self, request):
        # cognito에서 사용자 풀 list 가져오기
        client = boto3.client(
            'cognito-idp',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_COGNITO_REGION
        )

        # 사용자 풀의 유저 목록 가져오기
        response = client.list_users(
            UserPoolId=settings.AWS_USER_POOL_ID
        )

        # 사용자 풀의 유저 목록을 MySQL과 동기화하기
        users = response.get('Users', [])
        for user in users:
            attributes = {attr['Name']: unicode_to_string(attr['Value']) for attr in user['Attributes']}
            user_id = user['Username']
            name = attributes.get('name', '')
            email = attributes.get('email', '')

            query = f"""
            INSERT INTO `User` (UserID, Name, Email) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                Name = VALUES(Name),
                Email = VALUES(Email)
            """

            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, [user_id, name, email])
                    connection.commit()
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                continue  # 이미 존재하는 사용자에 대해서는 계속 진행

        return Response({"message": "Users synchronized successfully"}, status=status.HTTP_200_OK)