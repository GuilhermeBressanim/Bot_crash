import scraper
import pandas as pd
import time
import botTelegram
import geraLog
import requests
import pytz
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
timezone = pytz.timezone('America/Sao_Paulo')


def avisaCrash(lista):
    try:
        dados = requests.get(
            os.environ['link_api']+'mostra_resultadosCrash').json()
        vezesMenor10 = 0
        vezesVela10 = 0
        vela = 0
        velaHora = 0
        for i, j in lista:
            if (float(j.Valores) < 10):
                vezesMenor10 += 1
            else:
                vela = (float(j.Valores))
                velaHora = j.Horas
                vezesVela10 += 1
                vezesMenor10 = 0
            ultimo = {
                "valores": j.Valores,
                "hora": j.Horas,
                "ultimoMaior": velaHora
            }
        try:
            if (int((str(dados['hora'][-1])).replace(" ", "").replace(":", ""))) != (int(str(ultimo['hora'][-8:]).replace(":", ""))):
                requests.post(os.environ['link_api'] +
                              'salva_resultadoCrash', json=ultimo)
        except:
            geraLog.geraLog("ERRO AO SALVAR OS VALORES DO KITBLAZE AS " +
                            datetime.now(timezone).strftime('%d/%m/%Y %H:%M:%S'))
        resultado = True
        aux = requests.get(
            os.environ['link_api']+'mostra_velas').json()
        aux = aux['quantidade'][-1]
        if (vezesMenor10 != 0):
            if ((vezesMenor10 in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]) and (aux == '0')):
                resultado = botTelegram.enviarMensagem(
                    "🚨🚨🚨 HORA DE APOSTAR MERMÃO, " + str(vezesMenor10) + " VELAS SEM 10X 🚨🚨🚨")
                ultimo = {'quantidade': '1'}
                requests.post(os.environ['link_api'] +
                              'salva_vela', json=ultimo)
            elif ((vezesMenor10 not in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]) and (aux == '1')):
                ultimo = {'quantidade': '0'}
                requests.post(os.environ['link_api'] +
                              'salva_vela', json=ultimo)

        else:
            if (vezesVela10 >= 1):
                if (int((str(dados['ultimoMaior'][-1])).replace(" ", "").replace(":", ""))) != (int(str(velaHora).replace(":", " ").replace(" ", ""))):
                    resultado = botTelegram.enviarMensagem(
                        "🌝🌝🌝 VELA DE " + str(vela) + " CM NA SUA CARA 🌝🌝🌝 ")
        if (not resultado):
            geraLog.geraLog("ERRO AO ENVIAR A MENSAGEM AS : " +
                            datetime.now(timezone).strftime('%H:%M'))
    except:
        geraLog.geraLog("ERRO AO SALVAR OS VALORES DO KITBLAZE AS " +
                        datetime.now(timezone).strftime('%d/%m/%Y %H:%M:%S'))


def start_notification():
    antigo = pd.DataFrame({
        'Valores': list(),
        'Hora': list(),
        "ultimoMaior": list()
    })

    atual = pd.DataFrame({
        'Valores': list(),
        'Hora': list(),
        "ultimoMaior": list()
    })

    botTelegram.enviarMensagem("BOT INICIADO")

    while (True):
        try:
            atual = scraper.pegaValoresKitBlaze()[::-1]
        except:
            geraLog.geraLog("ERRO AO PEGAR OS VALORES DO KITBLAZE AS " +
                            datetime.now(timezone).strftime('%d/%m/%Y %H:%M:%S'))
            atual = antigo.copy()[::-1]
            time.sleep(1)
        if (not atual.equals(antigo)):
            # diferentes = pd.concat([atual, antigo]).drop_duplicates(keep=False)
            antigo = atual.copy()[::-1]
            avisaCrash((atual.iterrows()))
            time.sleep(5)
        time.sleep(1)


if (__name__ == '__main__'):
    start_notification()
