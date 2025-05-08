from django.db import connection
from django.core.cache import cache
from django.conf import settings
from datetime import datetime
import redis as redis_lib
import requests
from urllib.parse import urljoin


def run_health_check():
    health = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': False,
        'cache': False,
        'redis': False,
    }

    # DB Check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            health['database'] = True
    except Exception as e:
        health['database_error'] = str(e)

    # Cache Check
    try:
        cache.set('health_check', 'ok', timeout=5)
        if cache.get('health_check') == 'ok':
            health['cache'] = True
    except Exception as e:
        health['cache_error'] = str(e)

    # Redis Check
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

    all_ok = all([health['database'], health['redis']])
    health['status'] = 'ready' if all_ok else 'not_ready'

    # Send status to main app API
    try:
        CORE_URL = settings.CORE_URL
        endpoint = urljoin(CORE_URL, "/receive-health-status/")
        response = requests.post(
            endpoint,
            json=health,
            headers={'Authorization': f'Bearer {settings.MAIN_APP_API_TOKEN}'}
        )
        health['report_response'] = response.status_code
    except Exception as e:
        health['report_error'] = str(e)

    return health
