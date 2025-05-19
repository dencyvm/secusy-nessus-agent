from django.db import connection
from django.core.cache import cache
from datetime import datetime
import redis as redis_lib
from django.conf import settings


def perform_health_check():
    health = {
        'scanner': 'nessus',
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

    # Redis check
    try:
        r = redis_lib.StrictRedis(
            host='redis',
            port=6379,
            password=settings.REDIS_PASSWORD,
            socket_connect_timeout=2
        )
        r.set("health_check_key", "ok", ex=5)
        if r.get("health_check_key") == b"ok":
            health['redis'] = True
    except Exception as e:
        health['redis_error'] = str(e)

    # Determine readiness
    all_ok = all([health['database'], health['redis']])
    health['status'] = 'ready' if all_ok else 'not_ready'

    return health
