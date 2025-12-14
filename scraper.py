import requests
from bs4 import BeautifulSoup
import json

# Fuente: Levvvel (La mejor base de datos, pero limpiaremos su basura)
URL = "https://levvvel.com/coin-master-free-spins/"

def update_spins():
    try:
        # 1. Nos disfrazamos de navegador PC para que nos den la web completa
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rewards = []
        all_links = soup.find_all('a')
        
        found_urls = set() 
        
        for link in all_links:
            href = link.get('href')
            text = link.get_text().strip().lower()
            
            if not href: continue

            # --- FILTRO MAESTRO (ANTI-PUBLICIDAD) ---

            # 1. REGLA DE ORO: Si el link se queda en "levvvel.com", ES BASURA (Menú/Noticia/Publicidad).
            if "levvvel.com" in href: continue

            # 2. REGLA DE PLATA: Solo queremos links que vayan al servidor del juego
            # Los links oficiales siempre contienen "moonactive" o "coinmaster.com"
            is_game_link = "moonactive" in href or "coinmaster.com" in href

            # 3. Validar texto (Spins/Coins) para asegurarnos
            is_reward_text = "spin" in text or "coin" in text

            # Solo guardamos si es un link OFICIAL del juego
            if is_game_link:
                
                if href in found_urls: continue
                
                # Crear título bonito
                pretty_title = link.get_text().strip().title()
                
                # Si el link no tiene texto, le ponemos uno genérico
                if len(pretty_title) < 4: 
                    pretty_title = "¡Premio Sorpresa!"

                rewards.append({
                    "title": pretty_title, # Saldrá "25 Spins", etc.
                    "url": href,           # Link directo (sin publicidad)
                    "date": "Disponible"
                })
                found_urls.add(href)

        # Guardar los últimos 15 (Los más nuevos)
        final_rewards = rewards[:15]

        with open('rewards.json', 'w') as f:
            json.dump(final_rewards, f, indent=2)
            
        print(f"¡Limpieza total! Se guardaron {len(final_rewards)} premios DIRECTOS (Sin publicidad).")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_spins()

if __name__ == "__main__":
    update_spins()
