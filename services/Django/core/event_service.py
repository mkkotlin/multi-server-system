import requests
from django.conf import settings

def publish_event(event_type, entity_type, entity_id, payload, source="django-service",):
    url = f"{settings.NODE_EVENT_SERVER_URL}/internal/events"
    data = {
        "eventType": event_type,
        "source": source,
        "entityType": entity_type,
        "entityId": str(entity_id),
        "payload": payload,
    }

    headers = {
        "X-Service-Key": settings.NODE_SERVICE_KEY,
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=5,)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print(f"Failed to publish event: {error}")
        return None