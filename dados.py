import requests
from datetime import datetime

def data_de_hoje():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def dados():
    data_hoje = data_de_hoje()
    
    # Faz a requisição
    r = requests.get("https://www.mpdft.mp.br/acompanhamento-sus-df/api/cns/solicitacoes-atuais/?cns=700008748692306&offset=0&next=10")
    solicitacoes = r.json()
    
    # Salva no arquivo
    with open("historico.txt", "a", encoding="utf-8") as historico:
        for solicitacao in solicitacoes:
            procedimento = solicitacao.get("procedimento")
            posicao = solicitacao.get("posicao")
            historico.write(f"{data_hoje},{procedimento},{posicao}\n")

if __name__ == "__main__":
    dados()
