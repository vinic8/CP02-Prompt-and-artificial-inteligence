"""
report.py — Geração de tabelas CSV e gráficos comparativos
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
GRAFICOS_DIR = os.path.join(OUTPUT_DIR, "graficos")
os.makedirs(GRAFICOS_DIR, exist_ok=True)


def gerar_tabela(resultados: list[dict]) -> pd.DataFrame:
    """Cria DataFrame, exibe no terminal e salva CSV."""
    df = pd.DataFrame(resultados)
    csv_path = os.path.join(OUTPUT_DIR, "resultados.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print("\n📊 TABELA COMPARATIVA")
    print(df.to_string(index=False))
    print(f"\n✅ CSV salvo em: {csv_path}")
    return df


def grafico_acuracia(df: pd.DataFrame):
    """Barras agrupadas: acurácia média por técnica × tarefa."""
    fig, ax = plt.subplots(figsize=(10, 5))
    tarefas = df["tarefa"].unique()
    tecnicas = df["tecnica"].unique()
    x = range(len(tarefas))
    width = 0.2

    for i, tec in enumerate(tecnicas):
        valores = [
            df[(df["tarefa"] == t) & (df["tecnica"] == tec)]["acuracia"].mean()
            for t in tarefas
        ]
        ax.bar([xi + i * width for xi in x], valores, width, label=tec)

    ax.set_xticks([xi + width for xi in x])
    ax.set_xticklabels(tarefas, rotation=15, ha="right")
    ax.set_ylabel("Acurácia média")
    ax.set_title("GameForge AI — Acurácia por Técnica × Tarefa")
    ax.legend()
    ax.set_ylim(0, 1.1)
    plt.tight_layout()
    path = os.path.join(GRAFICOS_DIR, "acuracia.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"📈 Gráfico salvo: {path}")


def grafico_custo(df: pd.DataFrame):
    """Barras: tokens médios (prompt + resposta) por técnica."""
    df["tokens_total"] = df["tokens_prompt"] + df["tokens_resposta"]
    resumo = df.groupby("tecnica")["tokens_total"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(resumo["tecnica"], resumo["tokens_total"], color=["#4C72B0", "#DD8452", "#55A868", "#C44E52"])
    ax.set_ylabel("Tokens médios por chamada")
    ax.set_title("GameForge AI — Custo de Tokens por Técnica")
    for i, v in enumerate(resumo["tokens_total"]):
        ax.text(i, v + 1, f"{v:.0f}", ha="center", fontsize=9)
    plt.tight_layout()
    path = os.path.join(GRAFICOS_DIR, "custo_tokens.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"📈 Gráfico salvo: {path}")


def grafico_temperatura(resultados_temp: list[dict]):
    """Linha: consistência por temperatura."""
    if not resultados_temp:
        return
    df_t = pd.DataFrame(resultados_temp)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df_t["temperatura"], df_t["consistencia"], marker="o", linewidth=2, color="#4C72B0")
    ax.set_xlabel("Temperatura")
    ax.set_ylabel("Consistência (0–1)")
    ax.set_title("GameForge AI — Consistência × Temperatura")
    ax.set_ylim(0, 1.1)
    plt.tight_layout()
    path = os.path.join(GRAFICOS_DIR, "temperatura.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"📈 Gráfico salvo: {path}")


def recomendar(df: pd.DataFrame) -> dict:
    """
    Retorna melhor técnica por tarefa com base em acurácia média.
    Também considera consistência como desempate.
    """
    recomendacoes = {}
    for tarefa in df["tarefa"].unique():
        sub = df[df["tarefa"] == tarefa].copy()
        resumo = (
            sub.groupby("tecnica")
            .agg(acuracia_media=("acuracia", "mean"), consistencia_media=("consistencia", "mean"))
            .reset_index()
            .sort_values(["acuracia_media", "consistencia_media"], ascending=False)
        )
        melhor = resumo.iloc[0]
        recomendacoes[tarefa] = {
            "tecnica": melhor["tecnica"],
            "acuracia_media": round(melhor["acuracia_media"], 2),
            "consistencia_media": round(melhor["consistencia_media"], 2),
            "justificativa": (
                f"Técnica '{melhor['tecnica']}' obteve maior acurácia média "
                f"({melhor['acuracia_media']:.0%}) e consistência "
                f"({melhor['consistencia_media']:.0%}) para a tarefa '{tarefa}'."
            ),
        }

    print("\n🏆 RECOMENDAÇÕES POR TAREFA")
    for tarefa, rec in recomendacoes.items():
        print(f"  [{tarefa}] → {rec['tecnica']} | {rec['justificativa']}")

    return recomendacoes
