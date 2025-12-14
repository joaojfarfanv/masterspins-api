import requests
from bs4 import BeautifulSoup
import json

# Fuente de los links
URL = "https://levvvel.com/coin-master-free-spins/"

def update_spins():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        rewards = []
        cards = soup.find_all('div', class_='daily-rewards-row')

        for card in cards:
            link_tag = card.find('a', href=True)
            if not link_tag: continue

            url = link_tag['href']
            if "moonactive" in url or "coin-master" in url:
                # Título simple
                rewards.append({
                    "title": "Tiradas Gratis",
                    "url": url,
                    "date": "Hoy"
                })

        # Guardar archivo
        with open('rewards.json', 'w') as f:
            json.dump(rewards, f, indent=2)

        print("¡Actualizado!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_spins()
