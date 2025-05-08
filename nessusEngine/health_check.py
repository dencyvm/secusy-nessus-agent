from django.db import connection
from django.core.cache import cache
from django.conf import settings
from datetime import datetime
import redis as redis_lib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def health_check(request):
    health = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': False,
        'cache': False,
        'redis': False,
    }

    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            health['database'] = True
    except Exception as e:
        health['database_error'] = str(e)

    # Cache check
    try:
        cache.set('health_check', 'ok', timeout=5)
        if cache.get('health_check') == 'ok':
            health['cache'] = True
    except Exception as e:
        health['cache_error'] = str(e)

    try:
        r = redis_lib.StrictRedis(
            host='redis',  # container name as hostname (matches docker-compose service name)
            port=6379,
            password=settings.REDIS_PASSWORD,
            socket_connect_timeout=2
        )
        r.set("health_check_key", "ok", ex=5)
        if r.get("health_check_key") == b"ok":
            health['redis'] = True
    except Exception as e:
        health['redis_error'] = str(e)

    all_ok = all([health['database'], health['redis']])
    health['status'] = 'ready' if all_ok else 'not_ready'
    return Response(health, status=status.HTTP_200_OK if all_ok else status.HTTP_503_SERVICE_UNAVAILABLE)