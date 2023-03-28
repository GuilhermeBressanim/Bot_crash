import requests
from bs4 import BeautifulSoup
import pandas as pd


def pegaValoresKitBlaze():
    page = requests.get('https://kitblaze.com/crash/')
    soup = BeautifulSoup(page.text, "html.parser")
    girosBlaze = soup.find(id="listagem_crasheds")
    listaValores = list()
    listaHoras = list()
    lis = girosBlaze.find_all("div", attrs={"class": "pdi-crash"})

    for i in lis:
        texto = i.get_text()
        valor = texto[1:7].strip().replace("X", "")
        hora = texto[-9:].strip()
        listaValores.append(valor)
        listaHoras.append(hora)

    df = pd.DataFrame({
        'Valores': listaValores,
        'Horas': listaHoras,
    })

    return df
