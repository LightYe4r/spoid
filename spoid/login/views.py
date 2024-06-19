import json
import boto3
from django.conf import settings
from django.http import JsonResponse
from botocore.exceptions import ClientError

def unicode_to_string(value):
    try:
        return value.encode('latin1').decode('unicode_escape')
    except Exception:
        return value

def get_user_info(request):
    try:
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

        users = response.get('Users', [])

        # 유저 정보 반환
        user_info = []
        for user in users:
            attributes = {attr['Name']: unicode_to_string(attr['Value']) for attr in user['Attributes']}
            user_info.append({
                'Attributes': attributes
            })

        return JsonResponse({'users': user_info})

    except ClientError as e:
        return JsonResponse({'error': str(e)}, status=400)
