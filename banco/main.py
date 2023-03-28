import sqlite3
import pytz
import pandas as pd
import os
from datetime import datetime
from flask import Flask, request, Response
from waitress import serve

app = Flask(__name__)
timezone = pytz.timezone('America/Sao_Paulo')
cwd = os.getcwd()


@app.route('/salva_resultadoCrash', methods=['POST'])
def salva_resultadoCrash():
    conn = sqlite3.connect(
        cwd + "/banco/base.db")
    cursor = conn.cursor()
    request_data = request.get_json()
    sql2 = 'INSERT INTO crash VALUES(" ' + request_data['valores']+' "," ' + request_data['hora'] + \
        ' "," '+request_data['ultimoMaior'] + ' ")'
    cursor.execute(sql2)
    conn.commit()
    conn.close()
    return Response(status=200)


@app.route('/mostra_resultadosCrash', methods=['GET'])
def mostra_resultadosCrash():
    conn = sqlite3.connect(
        cwd + "/banco/base.db")
    cursor = conn.cursor()
    lista = cursor.execute("SELECT * FROM crash").fetchall()
    conn.close()
    resultado = {
        'valores': list(pd.DataFrame(lista).iloc[-2000:][0]),
        'hora': list(pd.DataFrame(lista).iloc[-2000:][1]),
        'ultimoMaior': list(pd.DataFrame(lista).iloc[-2000:][2])
    }
    return (resultado)


@app.route('/salva_vela', methods=['POST'])
def salva_velas():
    conn = sqlite3.connect(
        cwd + "/banco/base.db")
    cursor = conn.cursor()
    request_data = request.get_json()
    sql2 = 'INSERT INTO velas VALUES('+request_data['quantidade']+')'
    cursor.execute(sql2)
    conn.commit()
    conn.close()
    return Response(status=200)


@app.route('/mostra_velas', methods=['GET'])
def mostra_vela():
    conn = sqlite3.connect(
        cwd + "/banco/base.db")
    cursor = conn.cursor()
    lista = cursor.execute("SELECT * FROM velas").fetchall()
    conn.close()
    resultado = {
        'quantidade': list(pd.DataFrame(lista).iloc[-2000:][0])
    }
    return (resultado)


serve(app, port=5000)
