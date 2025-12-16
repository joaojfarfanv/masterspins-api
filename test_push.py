import requests
import json

# TUS CREDENCIALES
ONESIGNAL_APP_ID = "7d8ae299-535f-4bbf-a14b-28852b836721"

# Pega aquí la llave larga que copiaste de la foto (la que empieza por os_v2...)
ONESIGNAL_API_KEY = "os_v2_app_pwfofgktl5f37iklfccsxa3heh4u2gairwjeqv4nendwoqymz65uqdpx3sutokduinay65ksui4zhy4vf4xwv2geu3f67d5il6hif5i"

def test_notification():
    header = {
        "Content-Type": "application/json; charset=utf-8",
        # CAMBIO CLAVE: Para llaves 'os_v2...', se usa "Bearer"
        "Authorization": f"Bearer {ONESIGNAL_API_KEY}"
    }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "headings": {"en": "🔔 Test Final"},
        "contents": {"en": "¡Funcionó con Bearer!"},
        "included_segments": ["Total Subscriptions"]
    }
    
    try:
        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
        print(f"Estado: {req.status_code}")
        print(req.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_notification()
