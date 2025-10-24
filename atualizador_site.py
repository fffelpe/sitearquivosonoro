import os
import logging
import requests

logging.basicConfig(filename="atualizador.log", level=logging.INFO)

API_KEY = "18cf1c24997095d2379003fa63adb584"

def buscar_imagem_artista(nome):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.getInfo",
        "artist": nome,
        "api_key": API_KEY,
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        dados = r.json()
        imagens = dados.get("artist", {}).get("image", [])
        return imagens[-1].get("#text", "") if imagens else ""
    except Exception as e:
        logging.warning(f"Erro ao buscar imagem de {nome}: {e}")
        return ""

def gerar_md(nome, imagem):
    os.makedirs("content", exist_ok=True)
    with open(f"content/{nome.lower()}.md", "w", encoding="utf-8") as f:
        f.write(f"""---
title: "{nome}"
date: 2025-10-24
image: "{imagem}"
---

Página gerada automaticamente para o artista {nome}.
""")

def main():
    artista = "Radiohead"
    imagem = buscar_imagem_artista(artista)
    gerar_md(artista, imagem)
    logging.info(f"Conteúdo gerado para {artista}")

if __name__ == "__main__":
    main()
