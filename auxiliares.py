from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
import os

load_dotenv(override=True)
cns = os.getenv("CNS")

NOME_ARQUIVO = Path("historico.txt")

def dados():
    try:
        r = requests.get(
            f"https://www.mpdft.mp.br/acompanhamento-sus-df/api/cns/solicitacoes-atuais/?cns={cns}&offset=0&next=10",
            timeout=10,
        )
        solicitacoes = r.json()
    except Exception as e:
        print(f"Erro ao buscar dados da API: {e}")
        return
    
    data_hoje = datetime.now()
    
    with open(NOME_ARQUIVO, "a", encoding="utf-8") as historico:
        for s in solicitacoes:
            procedimento = s.get("procedimento")
            posicao = s.get("posicao")
            if procedimento and posicao is not None:
                historico.write(f"{data_hoje},{procedimento.strip()},{posicao}\n")

def data_de_hoje():
 
    return datetime.now()

#Adiciona coluna com apenas a data 
def adiciona_data(dados): 
    
    dados['datetime'] = pd.to_datetime(dados['datetime'])
    dados['data'] = dados['datetime'].dt.date
    return dados 