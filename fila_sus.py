from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

def data_de_hoje():
    
    return datetime.now()

def dados():
    
    data_hoje = data_de_hoje()
    
    r = requests.get("https://www.mpdft.mp.br/acompanhamento-sus-df/api/cns/solicitacoes-atuais/?cns=700008748699999&offset=0&next=10")
    solicitacoes = r.json()
    # print(solicitacoes)
    
    with open("historico.txt", "a",encoding="utf-8") as historico:
        for solicitacao in solicitacoes:
            procedimento = solicitacao.get("procedimento")
            posicao = solicitacao.get("posicao")
            historico.write(f"{data_hoje},{procedimento},{posicao}\n")
            
  
def grafico_individual(df):
    
    df.plot(title='Posição na Fila - Eletrocardiograma',
            x='data',
            y='posicao',
            kind='scatter',
            xlabel='Data',
            ylabel='Posição',
            marker='o',
            rot=45,
            grid=True)
    
    plt.tight_layout()
    plt.show()
    
    
def dataframes_individuais():
    
    dados = pd.read_csv("historico.txt")
    dados['datetime'] = pd.to_datetime(dados['datetime'])
    dados['data'] = dados['datetime'].dt.date
    
    # print(dados)
    
    #ELETROCARDIOGRAMA
    df1 = dados[dados['procedimento'] == 'ELETROCARDIOGRAMA']
    # print(df1)
    
    #CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO
    df2 = dados[dados['procedimento'] == 'CONSULTA EM CARDIOLOGIA - RISCO CIRURGICO']
    # print(df2)
    
    #ENDOSCOPIA DIGESTIVA ALTA
    df3 = dados[dados['procedimento'] == 'ENDOSCOPIA DIGESTIVA ALTA']
    # print(df3)
    
    #CONSULTA EM PSIQUIATRIA - GERAL
    df4 = dados[dados['procedimento'] == 'CONSULTA EM PSIQUIATRIA - GERAL']
    # print(df4)
    
    # grafico_individual(df1)
    
    grafico_individual(df2)
    
# dados()    
dataframes_individuais()
