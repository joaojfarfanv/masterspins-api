import requests
from bs4 import BeautifulSoup
import json

URL = "https://levvvel.com/coin-master-free-spins/"

def update_spins():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rewards = []
        all_links = soup.find_all('a')
        
        rewards_found = 0
        MAX_REWARDS = 50 

        for link in all_links:
            if rewards_found >= MAX_REWARDS: break
            
            href = link.get('href')
            if not href: continue
            
            text = link.get_text().strip()

            # --- CORRECCIÓN CRÍTICA ---
            # 1. Solo aceptamos enlaces que vayan a los servidores del juego (moonactive)
            # 2. PROHIBIMOS enlaces que contengan "levvvel" (para que no abra la web de noticias)
            is_game_link = "moonactive" in href 
            
            # Filtro extra: a veces los enlaces del juego vienen vacíos de texto,
            # pero si la URL es correcta, nos sirve igual.
            if is_game_link:
                # Crear un título bonito
                title = text
                if not title or "collect" in title.lower() or len(title) < 5:
                    title = "Tiradas y Monedas Gratis"
                
                # Evitar duplicados
                is_duplicate = any(r['url'] == href for r in rewards)
                
                if not is_duplicate:
                    rewards.append({
                        "title": title,
                        "url": href, # Este link abrirá la app directamente
                        "date": "Disponible"
                    })
                    rewards_found += 1

        # Guardar todo
        with open('rewards.json', 'w') as f:
            json.dump(rewards, f, indent=2)
            
        print(f"¡Éxito! Se encontraron {len(rewards)} premios OFICIALES.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_spins()

if __name__ == "__main__":
    update_spins()
