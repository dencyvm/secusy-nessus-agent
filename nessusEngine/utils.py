import datetime
import jwt
from django.conf import settings

def generate_jwt_service_token():
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        # 'iat': int(now.timestamp()),  # Convert datetime to timestamp
        'exp': int((now + datetime.timedelta(minutes=15)).timestamp())  # Convert datetime to timestamp
    }
    token = jwt.encode(payload, settings.JWT_SERVICE_SECRET, algorithm='HS256')
    return token