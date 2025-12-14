import requests
from bs4 import BeautifulSoup
import json

# Usaremos LEVVVEL que es muy estable, pero con una búsqueda más agresiva
URL = "https://levvvel.com/coin-master-free-spins/"

def update_spins():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rewards = []
        
        # ESTRATEGIA V2: Buscar todos los enlaces que digan "Collect" o "Spins"
        # Esto funciona aunque cambien el diseño (divs, clases, tablas)
        all_links = soup.find_all('a')

        count = 0
        for link in all_links:
            if not link.get('href'): continue
            
            text = link.get_text().strip().lower()
            href = link['href']

            # Filtros para saber si es un premio real
            is_reward = "collect" in text or "spins" in text
            is_valid_url = href.startswith("http") and ("levvvel" in href or "moonactive" in href)

            if is_reward and is_valid_url and count < 5: # Limitamos a los 5 más nuevos
                # Creamos un título genérico
                title = link.get_text().strip()
                if not title or title.lower() == "collect":
                    title = "Tiradas y Monedas Gratis"
                
                rewards.append({
                    "title": title,
                    "url": href,
                    "date": "Nuevo" 
                })
                count += 1

        # Si no encontramos nada, añadimos uno de prueba para que la App no se vea vacía
        if not rewards:
            rewards.append({
                "title": "Prueba de Sistema (No hay links detectados)",
                "url": "https://google.com",
                "date": "Hoy"
            })

        # Guardar archivo
        with open('rewards.json', 'w') as f:
            json.dump(rewards, f, indent=2)
            
        print(f"¡Actualizado! Se encontraron {len(rewards)} premios.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_spins()
