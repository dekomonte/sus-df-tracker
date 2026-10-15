# Versão do Gemini com instruções minhas de estimativa matemática e visualização
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from scipy.optimize import curve_fit
from datetime import datetime, timedelta
from pathlib import Path

NOME_ARQUIVO = Path("historico.txt")

def data_de_hoje():
    return datetime.now()


def modelo_exponencial(t, a, k):
    """Modelo de decaimento exponencial: y(t) = a * exp(-k * t)"""
    return a * np.exp(-k * t)


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

    with open(NOME_ARQUIVO, "a", encoding="utf-8") as f:
        for solicitacao in solicitacoes:
            procedimento = solicitacao.get("procedimento", "").strip()
            posicao = solicitacao.get("posicao")
            if procedimento and posicao is not None:
                f.write(f"{data_hoje.isoformat()}, {procedimento}, {posicao}\n")


def graficos():
    if not NOME_ARQUIVO.exists():
        print(f"Arquivo '{NOME_ARQUIVO}' não encontrado.")
        return

    data_hoje_str = datetime.now().strftime("%d/%m/%Y")

    # Leitura do histórico
    df = pd.read_csv(
        NOME_ARQUIVO,
        header=None,
        names=["data_hora", "procedimento", "posicao"],
        sep=r"\s*,\s*",
        engine="python",
        on_bad_lines="skip",
    )

    # Limpeza básica
    df["procedimento"] = df["procedimento"].str.strip()
    df["posicao"] = pd.to_numeric(df["posicao"], errors="coerce")
    df = df.dropna(subset=["posicao"])

    # Filtro de exclusão
    padrao_exclusao = r"ENDOSCOPIA|PSIQUIATR"
    df = df[~df["procedimento"].str.contains(padrao_exclusao, case=False, na=False)]

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
        # Consolida histórico por dia
        grupo_dia = (
            grupo.groupby("data_formatada", as_index=False)
            .agg({"posicao": "last", "data_dt": "last"})
            .sort_values("data_dt")
        )

        label_legenda = procedimento

        # ---------------------------------------------------------------------
        # ESTIMATIVA EXPONENCIAL DE ATENDIMENTO DA FILA
        # ---------------------------------------------------------------------
        if len(grupo_dia) >= 3:
            dias_decorridos = np.array(
                [(d - data_minima).total_seconds() / 86400.0 for d in grupo_dia["data_dt"]]
            )
            posicoes = grupo_dia["posicao"].values

            try:
                # Estimativas iniciais para otimização [a, k]
                p0 = [posicoes[0], 0.01]
                popt, _ = curve_fit(
                    modelo_exponencial,
                    dias_decorridos,
                    posicoes,
                    p0=p0,
                    bounds=(0, [np.inf, np.inf]),
                    maxfev=5000,
                )
                a_opt, k_opt = popt

                # Cálculo de R² para medir a qualidade do ajuste
                residuos = posicoes - modelo_exponencial(dias_decorridos, *popt)
                ss_res = np.sum(residuos**2)
                ss_tot = np.sum((posicoes - np.mean(posicoes)) ** 2)
                r_squared = 1 - (ss_res / (ss_tot + 1e-8))

                if k_opt > 1e-6:  # Fila reduzindo
                    # Calcula o dia t onde a posição atinge <= 1
                    t_alvo = np.log(a_opt) / k_opt
                    data_estimada = data_minima + timedelta(days=float(t_alvo))

                    if 0 <= t_alvo <= 3650:
                        qualidade = "" if r_squared >= 0.5 else " (Baixa Precisão)"
                        label_legenda += f"\n  └ Exp: {data_estimada.strftime('%d/%m/%Y')}{qualidade}"
                    else:
                        label_legenda += "\n  └ Exp: > 10 anos"
                else:
                    label_legenda += "\n  └ Exp: Fila Estagnada/Crescendo"

            except Exception:
                label_legenda += "\n  └ Exp: Erro no Ajuste"
        else:
            label_legenda += "\n  └ Exp: Dados Insuficientes (mín. 3)"

        # ---------------------------------------------------------------------

        # Plot da linha real
        linha = plt.plot(
            grupo_dia["data_formatada"],
            grupo_dia["posicao"],
            marker="o",
            linewidth=2,
            label=label_legenda,
        )
        cor_linha = linha[0].get_color()

        # Rótulo no último ponto
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

    plt.title(
        f"Evolução e Previsão Exponencial da Fila — Gerado em {data_hoje_str}",
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
        title="Procedimentos & Previsões Exponenciais",
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
