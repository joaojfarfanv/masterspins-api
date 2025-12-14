import requests
from bs4 import BeautifulSoup
import json

# Usamos Levvvel porque actualiza más rápido que nadie
URL = "https://levvvel.com/coin-master-free-spins/"

def update_spins():
    try:
        # Nos hacemos pasar por un navegador real de PC
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rewards = []
        # Buscamos TODOS los enlaces de la web
        all_links = soup.find_all('a')
        
        found_urls = set() # Para no repetir links
        
        for link in all_links:
            href = link.get('href')
            text = link.get_text().strip().lower() # Texto en minúsculas
            
            if not href: continue

            # --- LA LÓGICA MAESTRA ---
            
            # 1. ¿Es un link que habla de premios? (Busca "spin" o "coin")
            is_reward_text = "spin" in text or "coin" in text
            
            # 2. Palabras prohibidas (para no guardar guías o menús)
            bad_words = ["guide", "trick", "wiki", "strategy", "village", "cost", "event", "facebook", "twitter"]
            is_garbage = any(word in href.lower() for word in bad_words) or any(word in text for word in bad_words)

            # 3. Filtro de seguridad: El link debe ser largo (los links cortos suelen ser menús)
            is_good_length = len(href) > 15

            if is_reward_text and not is_garbage and is_good_length:
                
                # Si ya tenemos este link, pasamos al siguiente
                if href in found_urls: continue
                
                # CREAR TÍTULO: Usamos el texto original (Ej: "25 Spins")
                # .title() pone la primera letra en mayúscula
                pretty_title = link.get_text().strip().title()
                
                # Si el título es muy feo o vacío, ponemos uno por defecto
                if len(pretty_title) < 5: 
                    pretty_title = "Premio Sorpresa (Tiradas/Monedas)"

                rewards.append({
                    "title": pretty_title, # Aquí saldrá "50 Spins", "25 Spins", etc.
                    "url": href,
                    "date": "Disponible"
                })
                found_urls.add(href)

        # Limitamos a los últimos 15 premios para no llenar el celular de basura antigua
        final_rewards = rewards[:15]

        # Guardar archivo
        with open('rewards.json', 'w') as f:
            json.dump(final_rewards, f, indent=2)
            
        print(f"¡Éxito! Se encontraron {len(final_rewards)} premios variados.")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    update_spins()
