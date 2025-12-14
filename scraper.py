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
        
        # BUSCAMOS TODOS LOS ENLACES DE LA PÁGINA
        all_links = soup.find_all('a')
        
        # Aumentamos el límite a 50 para que traiga los de días anteriores
        count = 0
        MAX_LINKS = 50 

        for link in all_links:
            if count >= MAX_LINKS: break
            if not link.get('href'): continue
            
            href = link['href']
            text = link.get_text().strip()

            # LÓGICA V3: Aceptamos todo lo que parezca premio
            is_valid_url = "levvvel.com" in href or "moonactive" in href
            # Buscamos palabras clave en el texto O en la URL
            is_reward = "spin" in text.lower() or "coin" in text.lower() or "collect" in text.lower()

            if is_valid_url and is_reward:
                # Limpiamos el título
                title = text
                if "collect" in title.lower() or len(title) < 5:
                    title = "Tiradas y Monedas Gratis"
                
                # Evitamos duplicados exactos si la página repite links
                is_duplicate = any(r['url'] == href for r in rewards)
                
                if not is_duplicate:
                    rewards.append({
                        "title": title,
                        "url": href,
                        "date": "Disponible" # Simplificamos la fecha
                    })
                    count += 1

        # Guardamos todo
        with open('rewards.json', 'w') as f:
            json.dump(rewards, f, indent=2)
            
        print(f"¡Éxito! Se encontraron {len(rewards)} premios.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_spins()
