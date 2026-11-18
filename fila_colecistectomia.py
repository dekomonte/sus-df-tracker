from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

def data_de_hoje():
 
    return datetime.now()

#Adiciona coluna com apenas a data 
def adiciona_data(dados): 
    
    dados['datetime'] = pd.to_datetime(dados['datetime'])
    dados['data'] = dados['datetime'].dt.date
    return dados 

#Faz a requisicao no site do ministerio publico e salva os valores em um arquivo (historico.txt)
def dados():
    
    data_hoje = data_de_hoje()
    
    r = requests.get("https://www.mpdft.mp.br/acompanhamento-sus-df/api/cns/solicitacoes-atuais/?cns=700008748692306&offset=0&next=10")
    solicitacoes = r.json()
    # print(solicitacoes)
    
    with open("historico.txt", "a",encoding="utf-8") as historico:
        for solicitacao in solicitacoes:
            procedimento = solicitacao.get("procedimento")
            posicao = solicitacao.get("posicao")
            historico.write(f"{data_hoje},{procedimento},{posicao}\n")

def grafico_individual(df):
    
    titulo = df['procedimento'].iloc[0]
    
    ax = df.plot(title=titulo,
            x='data',
            y='posicao',
            linestyle='--',
            color='blue',
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
            fontsize=9,
            color='blue'
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