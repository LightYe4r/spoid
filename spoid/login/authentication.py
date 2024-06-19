import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
import boto3
from django.conf import settings

logger = logging.getLogger(__name__)

class CognitoJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        client = boto3.client('cognito-idp', region_name=settings.AWS_COGNITO_REGION)
        try:
            access_token = str(validated_token)
            user = client.get_user(AccessToken=access_token)
            logger.info(f"Authenticated user: {user['Username']}")
            return user['Username']
        except client.exceptions.NotAuthorizedException:
            logger.error("Invalid token")
            raise InvalidToken("Invalid token")
        except Exception as e:
            logger.error(f"Failed to validate token: {str(e)}")
            raise AuthenticationFailed(f"Failed to validate token: {str(e)}")
