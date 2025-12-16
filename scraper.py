import requests
from bs4 import BeautifulSoup
import json
import re
import os

# --- CONFIGURACIÓN ---
URL = "https://levvvel.com/coin-master-free-spins/"
JSON_FILE = 'rewards.json'

# Credenciales OneSignal (La configuración que YA CONFIRMAMOS que funciona)
ONESIGNAL_APP_ID = "7d8ae299-535f-4bbf-a14b-28852b836721"

# Tu llave tipo V2 (requiere Bearer)
ONESIGNAL_API_KEY = "os_v2_app_pwfofgktl5f37iklfccsxa3heeciqsusjyyeoee6wyaovhblhx5m4c4k5lyhdalchkymq3lumf36g46laxay6mljnvrjc2cevpbhhqq".strip()

def send_notification(title, url):
    """Envía notificación a todos los usuarios"""
    header = {
        "Content-Type": "application/json; charset=utf-8",
        # IMPORTANTE: Aquí está el cambio clave, usamos 'Bearer' en lugar de 'Key'
        "Authorization": f"Bearer {ONESIGNAL_API_KEY}"
    }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "headings": {"en": "🎁 ¡Nuevo Premio Disponible!", "es": "🎁 ¡Nuevo Premio Disponible!"},
        "contents": {"en": title, "es": title},
        "url": url,
        "included_segments": ["Total Subscriptions"]
    }
    try:
        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
        print(f"📡 Notificación enviada. Estado: {req.status_code}")
    except Exception as e:
        print(f"⚠️ Error enviando notificación: {e}")

def load_existing_urls():
    """Carga URLs ya guardadas para evitar duplicados"""
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
        
        # Buscar enlaces
        all_links = soup.find_all('a', href=True)
        count = 0
        new_reward_found = False
        
        for link in all_links:
            href = link['href']
            
            if "moonactive" in href or "coinmaster.com" in href:
                if href in current_found_urls: continue
                
                # --- OBTENER TÍTULO ---
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

                # --- ASIGNAR FECHA ---
                if count < 4: fecha = "HOY"
                elif count < 8: fecha = "AYER"
                else: fecha = "ANTERIOR"

                # Guardar en lista
                rewards.append({
                    "title": titulo_final,
                    "url": href,
                    "date": fecha
                })

                # --- LÓGICA DE NOTIFICACIÓN ---
                # Si es el primer link de la lista (el más reciente) y NO estaba en el JSON anterior:
                if count == 0 and href not in existing_urls:
                    print(f"🚀 ¡NUEVO PREMIO DETECTADO!: {titulo_final}")
                    send_notification(titulo_final, href)
                    new_reward_found = True

                current_found_urls.add(href)
                count += 1
                if count >= 30: break

        # Guardar JSON
        with open(JSON_FILE, 'w') as f:
            json.dump(rewards, f, indent=2)
            
        if new_reward_found:
            print(f"✅ Listo: Se enviaron notificaciones de nuevos premios.")
        else:
            print(f"✅ Listo: Base de datos actualizada (Sin premios nuevos).")

    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    update_spins()
