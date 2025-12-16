import requests
from bs4 import BeautifulSoup
import json
import re
import os

# --- CONFIGURACIÓN ---
URL = "https://levvvel.com/coin-master-free-spins/"
JSON_FILE = 'rewards.json'

# --- CREDENCIALES ---
ONESIGNAL_APP_ID = "7d8ae299-535f-4bbf-a14b-28852b836721"

# 🔒 SEGURIDAD MÁXIMA:
# Ahora el código busca la llave en los "Secretos" de GitHub.
# Ya NO la escribimos aquí para que no se borre ni te la roben.
ONESIGNAL_API_KEY = os.environ.get("ONESIGNAL_API_KEY")

def send_notification(title, url):
    """Envía notificación con DATA oculta para que abra la APP (Monetización)"""
    
    # Verificación de seguridad: Si no encuentra la llave en la caja fuerte, avisa.
    if not ONESIGNAL_API_KEY:
        print("❌ ERROR CRÍTICO: No se encontró la llave API.")
        print("👉 Si estás en tu PC: Configura la variable de entorno.")
        print("👉 Si estás en GitHub: Asegúrate de haber creado el Secret 'ONESIGNAL_API_KEY'.")
        return

    # Solo mostramos los últimos 5 caracteres para verificar que cargó bien
    print(f"🔑 Llave cargada desde Secrets (Termina en ...{ONESIGNAL_API_KEY[-5:]})") 
    
    header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {ONESIGNAL_API_KEY}"
    }
    
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "headings": {"en": "🎁 ¡Nuevo Premio!", "es": "🎁 ¡Nuevo Premio!"},
        "contents": {"en": "Toca aquí para reclamar tus tiradas", "es": "Toca aquí para reclamar tus tiradas"},
        
        # ✅ Enviamos el link en "data". Tu App debe leer "click_url".
        "data": {"click_url": url},
        
        "included_segments": ["Total Subscriptions"]
    }
    
    try:
        print("📡 Enviando petición a OneSignal (Modo App)...")
        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
        
        if req.status_code == 200:
            print(f"✅ ÉXITO: Notificación enviada. Al tocarla abrirá TU APP.")
        else:
            print(f"❌ FALLÓ (Estado {req.status_code})")
            print(f"🔍 Mensaje: {req.text}")
            
    except Exception as e:
        print(f"⚠️ Error de conexión: {e}")

def load_existing_urls():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r') as f:
                data = json.load(f)
                return {item['url'] for item in data}
        except:
            return set()
    return set()

def update_spins():
    try:
        print("🔄 Buscando nuevos premios...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rewards = []
        existing_urls = load_existing_urls()
        current_found_urls = set()
        
        all_links = soup.find_all('a', href=True)
        count = 0
        new_reward_found = False
        
        for link in all_links:
            href = link['href']
            
            if "moonactive" in href or "coinmaster.com" in href:
                if href in current_found_urls: continue
                
                texto = link.get_text().strip()
                parent_text = link.parent.get_text().strip() if link.parent else ""
                full_text = parent_text if ("Collect" in texto or len(texto) < 3) else texto
                
                titulo_final = "Premio Sorpresa"
                match = re.search(r'(\d+\s*(?:Spins|Tiradas|Coins|Monedas|M|K).*)', full_text, re.IGNORECASE)
                
                if match:
                    titulo_final = match.group(1).split("Collect")[0].strip()
                else:
                    titulo_final = full_text.replace("Collect", "").strip()

                if len(titulo_final) > 30: titulo_final = "Tiradas Gratis"

                if count < 4: fecha = "HOY"
                elif count < 8: fecha = "AYER"
                else: fecha = "ANTERIOR"

                rewards.append({
                    "title": titulo_final,
                    "url": href,
                    "date": fecha
                })

                if count == 0 and href not in existing_urls:
                    print(f"🚀 ¡NUEVO PREMIO DETECTADO!: {titulo_final}")
                    send_notification(titulo_final, href)
                    new_reward_found = True

                current_found_urls.add(href)
                count += 1
                if count >= 30: break

        with open(JSON_FILE, 'w') as f:
            json.dump(rewards, f, indent=2)
            
        if new_reward_found:
            print(f"✅ Proceso completado.")
        else:
            print(f"✅ Sin novedades.")

    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    update_spins()
