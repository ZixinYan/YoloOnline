from jwt import decode as jwt_decode
from rest_framework_jwt.settings import api_settings

def custom_jwt_decode_handler(token):
    return jwt_decode(
        token,
        api_settings.JWT_SECRET_KEY,
        algorithms=[api_settings.JWT_ALGORITHM]
    )
