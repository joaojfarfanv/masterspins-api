import requests
import json

# TUS CREDENCIALES
ONESIGNAL_APP_ID = "7d8ae299-535f-4bbf-a14b-28852b836721"

# Esta es tu llave nueva (la de la foto image_7f39a5.png)
# Le quitamos espacios por si acaso
ONESIGNAL_API_KEY = "os_v2_app_pwfofgktl5f37iklfccsxa3heet4opp4ylze6gvlsyyxhzieepx7nmnqoz6sfu5lelm4eapyvvlxwb54lwqbbb56iioxmpggldbolra".strip()

def test_notification():
    header = {
        "Content-Type": "application/json; charset=utf-8",
        # CORRECCIÓN: Cambiamos "Key" por "Bearer"
        "Authorization": f"Bearer {ONESIGNAL_API_KEY}"
    }
    
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "headings": {"en": "🔔 Prueba Final"},
        "contents": {"en": "¡Funciona con Bearer!"},
        "included_segments": ["Total Subscriptions"]
    }
    
    try:
        print("📡 Enviando con llave tipo V2 (Bearer)...")
        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
        
        print(f"Estado: {req.status_code}")
        print("Respuesta:", req.text)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_notification()
