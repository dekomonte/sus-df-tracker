#GitHub Actions 
import requests
from datetime import datetime

def data_de_hoje():
    return datetime.now()

def dados():
    data_hoje = data_de_hoje()

    # Faz a requisição
    r = requests.get("https://www.mpdft.mp.br/acompanhamento-sus-df/api/cns/solicitacoes-atuais/?cns=700008748692306&offset=0&next=10", timeout=30)
    solicitacoes = r.json()

    # Verifica se retornou dados
    if not solicitacoes:
        print("Nenhum dado retornado. Histórico não atualizado.")
        return

    # Salva no arquivo
    with open("historico.txt", "a", encoding="utf-8") as historico:
        for solicitacao in solicitacoes:
            procedimento = solicitacao.get("procedimento")
            posicao = solicitacao.get("posicao")
            historico.write(f"{data_hoje},{procedimento},{posicao}\n")

if __name__ == "__main__":
    dados()
