import requests
from bs4 import BeautifulSoup
import json
import datetime
import re

URL = "https://levvvel.com/coin-master-free-spins/"

# Diccionario para traducir meses de inglés (Levvvel) a número
MESES_EN = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

def obtener_fecha_bonita(texto_fecha):
    """Convierte 'Dec 15' a 'HOY', 'AYER' o '15 DIC'"""
    try:
        # Levvvel suele poner fechas tipo "Dec 15"
        partes = texto_fecha.split()
        if len(partes) < 2: return "Reciente"
        
        mes_str = partes[0]
        dia_num = int(partes[1])
        mes_num = MESES_EN.get(mes_str, 1)
        
        hoy = datetime.date.today()
        # Asumimos año actual
        fecha_premio = datetime.date(hoy.year, mes_num, dia_num)
        
        # Corrección por si el premio es de Dic y estamos en Ene (cambio de año)
        if fecha_premio > hoy:
            fecha_premio = datetime.date(hoy.year - 1, mes_num, dia_num)

        if fecha_premio == hoy:
            return "HOY"
        elif fecha_premio == hoy - datetime.timedelta(days=1):
            return "AYER"
        else:
            # Formato corto en español
            meses_es = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
            return f"{dia_num} {meses_es[mes_num - 1]}"
    except:
        return "HOY" # Si falla, asumimos hoy

def detectar_tipo(texto):
    """Define si es 'spin' o 'coin'"""
    t = texto.lower()
    if "coin" in t: return "coin"
    return "spin" # Por defecto tiradas

def update_spins():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rewards = []
        found_urls = set() 
        
        # 1. CAMBIO CLAVE: Buscamos filas de tabla (tr) para leer la FECHA
        filas = soup.find_all('tr')
        
        for fila in filas:
            columnas = fila.find_all('td')
            
            # Levvvel suele tener estructura: [Fecha] [Premio] [Botón]
            if len(columnas) >= 3:
                fecha_raw = columnas[0].get_text().strip()
                texto_premio = columnas[1].get_text().strip()
                
                # Buscar el link dentro de la columna del botón
                link_tag = columnas[2].find('a')
                if not link_tag: continue
                
                href = link_tag.get('href')
                if not href: continue

                # --- FILTRO ANTIGUO ---
                if "levvvel.com" in href: continue
                is_game_link = "moonactive" in href or "coinmaster.com" in href
                
                if is_game_link and href not in found_urls:
                    
                    # 2. LOGICA NUEVA: FECHA Y TIPO
                    fecha_final = obtener_fecha_bonita(fecha_raw)
                    tipo_final = detectar_tipo(texto_premio)
                    
                    # Limpieza título
                    titulo_bonito = texto_premio.title()
                    if len(titulo_bonito) < 4: titulo_bonito = "Premio Sorpresa"

                    rewards.append({
                        "title": titulo_bonito,
                        "url": href,
                        "date": fecha_final, # Ej: "HOY", "AYER"
                        "type": tipo_final   # Ej: "spin", "coin"
                    })
                    found_urls.add(href)

        # Guardar los últimos 40 (para tener historial de "Ayer")
        final_rewards = rewards[:40]

        with open('rewards.json', 'w') as f:
            json.dump(final_rewards, f, indent=2)
            
        print(f"¡Éxito! Se guardaron {len(final_rewards)} premios con fechas y tipos.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_spins()
