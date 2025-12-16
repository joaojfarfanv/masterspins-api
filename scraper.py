import requests
from bs4 import BeautifulSoup
import json
import re

URL = "https://levvvel.com/coin-master-free-spins/"

def update_spins():
    try:
        # Cabeceras para parecer un navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rewards = []
        found_urls = set()
        
        # BUSQUEDA AGRESIVA: Busca cualquier link que vaya al juego
        all_links = soup.find_all('a', href=True)
        
        # Contador para "adivinar" fechas si no las encontramos
        count = 0
        
        for link in all_links:
            href = link['href']
            
            # Filtro: Solo links de Moonactive o Coinmaster
            if "moonactive" in href or "coinmaster.com" in href:
                if href in found_urls: continue
                
                # 1. INTENTAR SACAR EL TÍTULO
                # A veces el texto está en el link, a veces en el padre
                texto = link.get_text().strip()
                parent_text = link.parent.get_text().strip() if link.parent else ""
                
                # Si el link dice "Collect", usamos el texto del contenedor padre
                if "Collect" in texto or len(texto) < 3:
                    full_text = parent_text
                else:
                    full_text = texto
                
                # Limpiamos el texto (Quitamos "Collect", fechas raras, etc)
                # Buscamos patrones como "25 Spins", "2M Coins"
                titulo_final = "Premio Sorpresa"
                match = re.search(r'(\d+\s*(?:Spins|Tiradas|Coins|Monedas).*)', full_text, re.IGNORECASE)
                if match:
                    titulo_final = match.group(1).split("Collect")[0].strip() # Limpieza extra
                else:
                    # Si no encuentra patrón, usa el texto bruto pero corto
                    titulo_final = full_text.replace("Collect", "").strip()
                    if len(titulo_final) > 30: titulo_final = "Tiradas Gratis"

                # 2. DEFINIR TIPO (Spin vs Coin)
                tipo = "spin"
                if "coin" in titulo_final.lower() or "moneda" in titulo_final.lower():
                    tipo = "coin"
                
                # 3. DEFINIR FECHA (Heurística: Los primeros son de Hoy)
                # Levvvel pone lo nuevo arriba.
                if count < 4:
                    fecha = "HOY"
                elif count < 8:
                    fecha = "AYER"
                else:
                    fecha = "ANTERIOR"

                rewards.append({
                    "title": titulo_final.title(),
                    "url": href,
                    "date": fecha,
                    "type": tipo
                })
                
                found_urls.add(href)
                count += 1
                
                # Limite de seguridad para no guardar basura antigua
                if count >= 30: break

        # Guardar JSON
        with open('rewards.json', 'w') as f:
            json.dump(rewards, f, indent=2)
            
        print(f"¡Recuperados {len(rewards)} premios! (Si sale 0, Levvvel cambió su código).")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    update_spins()
