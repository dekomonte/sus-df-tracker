# Versão do Gemini com instruções minhas de estimativa matemática e visualização
# (Caso seja necessário executar em outro ambiente)
import os
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

NOME_ARQUIVO = Path("historico.txt")


def data_de_hoje():
    return datetime.now()


def dados():
    data_hoje = data_de_hoje()
    url = (
        "https://www.mpdft.mp.br/acompanhamento-sus-df/api/cns/"
        "solicitacoes-atuais/?cns=700008748692306&offset=0&next=10"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        solicitacoes = response.json()
    except requests.RequestException as err:
        print(f"Erro ao consultar a API: {err}")
        return

    # Gravação otimizada para evitar duplicadas seguidas idênticas
    with open(NOME_ARQUIVO, "a", encoding="utf-8") as f:
        for solicitacao in solicitacoes:
            procedimento = solicitacao.get("procedimento", "").strip()
            posicao = solicitacao.get("posicao")
            if procedimento and posicao is not None:
                f.write(f"{data_hoje.strftime('%Y-%m-%d %H:%M:%S')}, {procedimento}, {posicao}\n")


def graficos():
    if not NOME_ARQUIVO.exists():
        print(f"Arquivo '{NOME_ARQUIVO}' não encontrado.")
        return

    data_hoje_str = datetime.now().strftime("%d/%m/%Y")

    # Leitura robusta do histórico
    df = pd.read_csv(
        NOME_ARQUIVO,
        header=None,
        names=["data_hora", "procedimento", "posicao"],
        sep=r"\s*,\s*",
        engine="python",
        on_bad_lines="skip",
    )

    # Limpeza e conversões
    df["procedimento"] = df["procedimento"].str.strip()
    df["posicao"] = pd.to_numeric(df["posicao"], errors="coerce")
    df = df.dropna(subset=["posicao"])

    # Exclusão de procedimentos indesejados
    procedimentos_ignorados = ["ENDOSCOPIA DIGESTIVA ALTA"]
    df = df[~df["procedimento"].isin(procedimentos_ignorados)]

    # Tratamento de datas
    df["data_dt"] = pd.to_datetime(df["data_hora"].str.strip(), errors="coerce")
    df = df.dropna(subset=["data_dt"])
    df = df.sort_values("data_dt")

    if df.empty:
        print("Nenhum dado válido para exibição.")
        return

    df["data_formatada"] = df["data_dt"].dt.strftime("%d/%m")
    data_minima = df["data_dt"].min()

    plt.figure(figsize=(12, 6))

    for idx, (procedimento, grupo) in enumerate(df.groupby("procedimento")):
        # Consolida registros por dia considerando o último valor gravado no dia
        grupo_dia = (
            grupo.groupby("data_formatada", as_index=False)
            .agg({"posicao": "last", "data_dt": "last"})
            .sort_values("data_dt")
        )

        label_legenda = procedimento

        # Regressão linear
        if len(grupo_dia) >= 2:
            dias_decorridos = np.array(
                [(d - data_minima).total_seconds() / 86400.0 for d in grupo_dia["data_dt"]]
            )
            posicoes = grupo_dia["posicao"].values

            slope, intercept = np.polyfit(dias_decorridos, posicoes, 1)

            if slope < 0:
                dia_alvo = (1 - intercept) / slope
                if 0 <= dia_alvo <= 3650:
                    try:
                        data_estimada = data_minima + timedelta(days=float(dia_alvo))
                        label_legenda += f"\n  └ Previsão: {data_estimada.strftime('%d/%m/%Y')}"
                    except OverflowError:
                        label_legenda += "\n  └ Previsão: > 10 anos"
                else:
                    label_legenda += "\n  └ Previsão: > 10 anos"
            else:
                label_legenda += "\n  └ Previsão: Fila Estagnada"
        else:
            label_legenda += "\n  └ Previsão: Dados insuficientes"

        # Plot da linha do procedimento
        linha = plt.plot(
            grupo_dia["data_formatada"],
            grupo_dia["posicao"],
            marker="o",
            linewidth=2,
            label=label_legenda,
        )
        cor_linha = linha[0].get_color()

        # Exibe o rótulo numérico apenas no ÚLTIMO PONTO (mais atualizado)
        ultimo_ponto = grupo_dia.iloc[-1]
        offset_y = 12 if idx % 2 == 0 else -18

        plt.annotate(
            str(int(ultimo_ponto["posicao"])),
            (ultimo_ponto["data_formatada"], ultimo_ponto["posicao"]),
            textcoords="offset points",
            xytext=(0, offset_y),
            ha="center",
            fontsize=9,
            color=cor_linha,
            weight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=cor_linha, lw=1, alpha=0.8),
        )

    # Configurações do layout
    plt.title(
        f"Evolução e Previsão da Posição na Fila de Espera — Atualizado em {data_hoje_str}",
        fontsize=13,
        pad=15,
        weight="bold",
    )
    plt.xlabel("Data (Dia/Mês)", fontsize=10)
    plt.ylabel("Posição na Fila", fontsize=10)

    ymin = max(0, df["posicao"].min() - 50)
    ymax = df["posicao"].max() + 50
    plt.ylim(ymin, ymax)

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(
        title="Procedimentos & Estimativas",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        fontsize=9,
    )
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    dados()
    graficos()
