import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://levvvel.com/coin-master-free-spins/"

def update_spins():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rewards = []
        found_urls = set()
        
        # Buscar enlaces
        all_links = soup.find_all('a', href=True)
        count = 0
        
        for link in all_links:
            href = link['href']
            
            # Solo links oficiales
            if "moonactive" in href or "coinmaster.com" in href:
                if href in found_urls: continue
                
                # --- OBTENER TÍTULO ---
                texto = link.get_text().strip()
                parent_text = link.parent.get_text().strip() if link.parent else ""
                
                if "Collect" in texto or len(texto) < 3:
                    full_text = parent_text
                else:
                    full_text = texto
                
                # Limpieza de texto (Buscar "25 Spins", "2M Coins", etc.)
                titulo_final = "Premio Sorpresa"
                match = re.search(r'(\d+\s*(?:Spins|Tiradas|Coins|Monedas|M|K).*)', full_text, re.IGNORECASE)
                
                if match:
                    titulo_final = match.group(1).split("Collect")[0].strip()
                else:
                    titulo_final = full_text.replace("Collect", "").strip()

                if len(titulo_final) > 30: titulo_final = "Tiradas Gratis"

                # --- ASIGNAR FECHA (Para agrupar en la App) ---
                if count < 4: fecha = "HOY"
                elif count < 8: fecha = "AYER"
                else: fecha = "ANTERIOR"

                # Guardamos sin preocuparnos del tipo (spin/coin)
                rewards.append({
                    "title": titulo_final,
                    "url": href,
                    "date": fecha
                })
                
                found_urls.add(href)
                count += 1
                if count >= 30: break

        # Guardar JSON
        with open('rewards.json', 'w') as f:
            json.dump(rewards, f, indent=2)
            
        print(f"¡Listo! {len(rewards)} premios guardados.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_spins()
