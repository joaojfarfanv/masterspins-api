import requests
import json

# TUS CREDENCIALES
ONESIGNAL_APP_ID = "7d8ae299-535f-4bbf-a14b-28852b836721" 
ONESIGNAL_API_KEY = "l55ihwmshellmbyom2ftbpso4"

def test_notification():
    header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Key {ONESIGNAL_API_KEY}"
    }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "headings": {"en": "🔔 Test de Prueba"},
        "contents": {"en": "Si lees esto, ¡funciona correctamente!"},
        "included_segments": ["Total Subscriptions"]
    }
    
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
    print(f"Estado: {req.status_code}")
    print(req.text)

if __name__ == "__main__":
    test_notification()
