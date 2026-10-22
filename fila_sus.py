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
            
#Gera grafico com todos procedimentos em aguardo
def grafico_geral(): 
    
    df = pd.read_csv("historico.txt")
    df = adiciona_data(df)
    
    # Remove ENDOSCOPIA DIGESTIVA ALTA pois ja foi feito
    df = df[df['procedimento'] != 'ENDOSCOPIA DIGESTIVA ALTA']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for procedimento, grupo in df.groupby('procedimento'):
        
        ax.plot(
            grupo['data'],
            grupo['posicao'],
            linestyle='--',
            marker='o',
            label=procedimento,
        ) 
        
    ax.set_title('Evolução da Posição na Fila do SUS-DF')
    ax.set_xlabel('Data')
    ax.set_ylabel('Posição')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title='Procedimentos') 
    plt.tight_layout()
    plt.show()

#Gera grafico individual para cada procedimento
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
       
#Cria dataframes individuais para cada procedimento
def dataframes():
    
    dados = pd.read_csv("historico.txt")
    dados = adiciona_data(dados)
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
    
    grafico_individual(df1)
    grafico_individual(df2)
    # grafico_individual(df3)
    # grafico_individual(df4)

    
dados()    
dataframes()
grafico_geral()
