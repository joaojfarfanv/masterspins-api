import requests
import json

# TUS CREDENCIALES
ONESIGNAL_APP_ID = "7d8ae299-535f-4bbf-a14b-28852b836721"
# Usamos la clave 'Python' que creaste en la imagen:
ONESIGNAL_API_KEY = "os_v2_app_pwfofgktl5f37iklfccsxa3hegvboqejq65ur34jvhfzpejvlosahn7dpf27j27az67yrvuwb44gxuqufhqryepixxlpzkfojnxuv3i"

def test_notification():
    header = {
        "Content-Type": "application/json; charset=utf-8",
        # CORRECCIÓN IMPORTANTE: Aquí debe decir "Basic", no "Key"
        "Authorization": f"Basic {ONESIGNAL_API_KEY}"
    }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "headings": {"en": "🔔 Test de Prueba"},
        "contents": {"en": "Si lees esto, ¡funciona correctamente!"},
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
