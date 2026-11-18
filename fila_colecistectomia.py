from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
from auxiliares import dados, data_de_hoje, adiciona_data

NOME_ARQUIVO = Path("historico.txt")

def grafico_individual(df):
    
    titulo = df['procedimento'].iloc[0]

    data_formatada = data_de_hoje().strftime("%d/%m/%Y")
    
    ax = df.plot(title=f'{titulo} {data_formatada}',
            x='data',
            y='posicao',
            linestyle='--',
            color='darkblue',
            kind='line',
            xlabel='Data',
            ylabel='Posição',
            marker='o',
            rot=45,
            grid=True)
    
   
    # GEMINI - Adicionar rótulos nos pontos de mudança de valor
    # Adicionar os rótulos intercalados (cima / baixo) 
    valores_exibidos = set()
    contador_rotulos = 0

    for x_val, y_val in zip(df["data"], df["posicao"]):
        # Se o valor já foi impresso em QUALQUER lugar do gráfico, pula
        if y_val in valores_exibidos:
            continue

        valores_exibidos.add(y_val)

        # Intercala a posição
        if contador_rotulos % 2 == 0:
            xytext = (0, 8)
            va = "bottom"
        else:
            xytext = (0, -12)
            va = "top"

        ax.annotate(
            str(y_val),
            (x_val, y_val),
            textcoords="offset points",
            xytext=xytext,
            ha="center",
            va=va,
            fontsize=10,
            color='darkblue'
        )

        contador_rotulos += 1
    
    plt.tight_layout()
    plt.show()

# Cria dataframes individuais para cada procedimento
def dataframes():
    
    dados = pd.read_csv("historico.txt")
    
    # Corrige o problema do decimal convertendo a posição para numérico e depois para inteiro
    dados["posicao"] = pd.to_numeric(dados["posicao"], errors="coerce")
    dados = dados.dropna(subset=["posicao"])
    dados["posicao"] = dados["posicao"].astype(int)
    
    dados = adiciona_data(dados)
    
    # Exemplo para a Colecistectomia
    dados["procedimento"] = dados["procedimento"].astype(str).str.strip()
    df = dados[dados["procedimento"] == "CE - COLECISTECTOMIA"]
    
    grafico_individual(df)

dados()    
dataframes()