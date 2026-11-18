# Versão do Gemini com instruções minhas de estimativa matemática e visualização
# (Caso seja necessário executar em outro ambiente)
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests

NOME_ARQUIVO = Path("historico.txt")


def dados():
    try:
        r = requests.get(
            "https://www.mpdft.mp.br/acompanhamento-sus-df/api/cns/solicitacoes-atuais/?cns=700008748692306&offset=0&next=10",
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


def graficos():
    
    if not NOME_ARQUIVO.exists():
        print(f"Arquivo '{NOME_ARQUIVO}' não encontrado.")
        return

    # Leitura e limpeza inicial do CSV
    df = pd.read_csv(
        NOME_ARQUIVO,
        header=None,
        names=["data_hora", "procedimento", "posicao"],
        on_bad_lines="skip",
    )
    
    df["procedimento"] = df["procedimento"].astype(str).str.strip()
    df["posicao"] = pd.to_numeric(df["posicao"], errors="coerce")
    df["data_dt"] = pd.to_datetime(df["data_hora"], errors="coerce")
    
    df = df.dropna(subset=["posicao", "data_dt"]).sort_values("data_dt")
    
    # Filtro de procedimentos indesejados
    procedimentos_ignorados = ["ENDOSCOPIA DIGESTIVA ALTA", "CE - COLECISTECTOMIA"]
    df = df[~df["procedimento"].isin(procedimentos_ignorados)]

    if df.empty:
        print("Nenhum dado válido para exibição.")
        return

    data_minima = df["data_dt"].min()
    plt.figure(figsize=(12, 6))

    for idx, (procedimento, grupo) in enumerate(df.groupby("procedimento")):
        # Consolida o último registro de cada dia
        grupo["data_dia"] = grupo["data_dt"].dt.normalize()
        grupo_dia = grupo.groupby("data_dia", as_index=False).agg({"posicao": "last", "data_dt": "last"})

        label_legenda = procedimento

        # Regressão linear
        if len(grupo_dia) >= 2:
            dias_decorridos = (grupo_dia["data_dt"] - data_minima).dt.total_seconds().values / 86400.0
            posicoes = grupo_dia["posicao"].values

            if np.ptp(dias_decorridos) > 0:
                slope, intercept = np.polyfit(dias_decorridos, posicoes, 1)

                if slope < 0:
                    dia_alvo = (1 - intercept) / slope
                    if 0 <= dia_alvo <= 3650:
                        data_estimada = data_minima + timedelta(days=float(dia_alvo))
                        label_legenda += f"\n  └ Previsão: {data_estimada.strftime('%d/%m/%Y')} (Regressão linear)"
                    else:
                        label_legenda += "\n  └ Previsão: > 10 anos"
                else:
                    label_legenda += "\n  └ Previsão: Fila Estagnada"
            else:
                label_legenda += "\n  └ Previsão: Dados insuficientes"
        else:
            label_legenda += "\n  └ Previsão: Dados insuficientes"

        # Plot da linha usando datas nativas do matplotlib
        linha = plt.plot(
            grupo_dia["data_dt"],
            grupo_dia["posicao"],
            marker="o",
            linewidth=2,
            label=label_legenda,
        )
        cor_linha = linha[0].get_color()

        # Rótulo numérico no último ponto
        ultimo = grupo_dia.iloc[-1]
        offset_y = 12 if idx % 2 == 0 else -18
        plt.annotate(
            str(int(ultimo["posicao"])),
            (ultimo["data_dt"], ultimo["posicao"]),
            textcoords="offset points",
            xytext=(0, offset_y),
            ha="center",
            fontsize=9,
            color=cor_linha,
            weight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=cor_linha, lw=1, alpha=0.8),
        )

    # Configuração inteligente do eixo X (resolve o excesso de labels)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))

    # Layout final
    plt.title(
        f"Evolução e Previsão da Posição na Fila de Espera SUS DF — Atualizado em {datetime.now().strftime('%d/%m/%Y')}",
        fontsize=13,
        pad=15,
        weight="bold",
    )
    plt.xlabel("Data", fontsize=10)
    plt.ylabel("Posição na Fila", fontsize=10)

    plt.ylim(max(0, df["posicao"].min() - 50), df["posicao"].max() + 50)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
    
    plt.gcf().autofmt_xdate()  # Rotaciona as datas automaticamente de forma elegante
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    dados()
    graficos()