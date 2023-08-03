import requests as req
import json
import os

with open("..\properties.json") as file:
    CONFIG = json.load(file)

JSON_PATH = CONFIG["JSON_PATH"]
PASTA_DESTINO = CONFIG["PASTA_DESTINO"]
SUFIXOS_EXTENSOES = [".jpg", ".png", ".jpeg"]
SUFIXO = ""

def carregar_dados_json():
    with open(JSON_PATH) as file:
        return json.load(file)

def calcular_capitulo_formatado(capitulo):
    capitulo_inteiro = int(capitulo)
    return f"{capitulo_inteiro:02d}"

def montar_url_base(manga):
    return f"{DATA['url']}{manga['prefixo']}{manga['nome']}"

def verificar_capitulo_existente(url_manga, capitulo):
    for sufixo in SUFIXOS_EXTENSOES:
        response = req.get(f"{url_manga}/capitulo-{capitulo}/1{sufixo}")
        if response.status_code == 200:
            return True

    return False

def baixar_capitulo(url_manga, nome, capitulo):
    pagina = 1
    while True:
        response, pagina_existe = verificar_pagina(url_manga, capitulo, pagina)

        if not pagina_existe:
            break

        nome_arquivo = f"{pagina:02d}{SUFIXO}"
        caminho_arquivo = f"{PASTA_DESTINO}/{nome}/{capitulo}/{nome_arquivo}"
        print(caminho_arquivo)

        with open(caminho_arquivo, "wb") as f:
            f.write(response.content)

        pagina += 1

def verificar_pagina(url_manga, capitulo, pagina):
    for sufixo in SUFIXOS_EXTENSOES:
        response = req.get(f"{url_manga}/capitulo-{capitulo}/{pagina}{sufixo}")


        if response.status_code == 200:
            global SUFIXO
            SUFIXO = sufixo
            return response, True

    return None, False

def criar_pasta(caminho):
    try:
        os.makedirs(caminho)
    except FileExistsError:
        print(f"A pasta {caminho} já existe.")

def baixar_manga(manga):
    nome = manga["nome"]
    capitulo = calcular_capitulo_formatado(manga["capitulo"])
    url_manga = montar_url_base(manga)

    while verificar_capitulo_existente(url_manga, capitulo):
        print(f"Baixando capitulo {capitulo} de {nome} em {PASTA_DESTINO}/{nome}/{capitulo}")
        criar_pasta(f"{PASTA_DESTINO}/{nome}/{capitulo}")
        baixar_capitulo(url_manga, nome, capitulo)
        capitulo = calcular_capitulo_formatado(int(capitulo) + 1)

    DATA["mangas"][mangas.index(manga)]["capitulo"] = int(capitulo) - 1
    gravar_json()

    print(f"Encerrado o download de {nome} no capitulo {int(capitulo) - 1}")

def gravar_json():

    with open(JSON_PATH, 'w') as file:
        json.dump(DATA, file, indent=4)

if __name__ == "__main__":
    print(CONFIG)
    DATA = carregar_dados_json()
    mangas = DATA["mangas"]

    for manga in mangas:
        print(f"Iniciando o download de {manga['nome']}")
        baixar_manga(manga)
