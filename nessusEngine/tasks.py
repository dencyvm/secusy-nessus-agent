import requests
from django.conf import settings
from nessusEngine.health_check import perform_health_check
from urllib.parse import urljoin
from nessusEngine.utils import generate_jwt_service_token


def send_health_to_core_app():
    health = perform_health_check()
    
    # Send the health data to the core app
    try:
        endpoint = urljoin(settings.CORE_URL, "/agent/receive-health-status/")
        service_token = generate_jwt_service_token()
        headers = {
            "org-id": settings.ORG_ID,
            "network-location": settings.NETWORK_LOCATION,
            "X-Service-Token": f"Bearer {service_token}"
        }
        response = requests.post(
            endpoint,  # Set this in your settings.py
            json=health,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        # Log error or handle it appropriately
        print(f"Health data send failed: {e}")
