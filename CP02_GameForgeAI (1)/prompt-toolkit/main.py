"""
main.py — GameForge AI · Prompt Toolkit
Ponto de entrada: executa todas as tarefas × técnicas × inputs e gera relatório.

Uso:
    python main.py
    python main.py --tarefa classificacao_feedback
    python main.py --dry-run   # simula sem chamar o LLM
"""
import argparse
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

from src.llm_client import LLMClient
from src.techniques import zero_shot, few_shot, chain_of_thought, role_prompting
from src.tasks import TAREFAS, get_tarefa
from src.evaluator import medir_acuracia, medir_consistencia, testar_temperatura, contar_tokens
from src.report import gerar_tabela, grafico_acuracia, grafico_custo, grafico_temperatura, recomendar

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def carregar_dados():
    with open(os.path.join(DATA_DIR, "inputs.json"), "r", encoding="utf-8") as f:
        inputs = json.load(f)
    with open(os.path.join(DATA_DIR, "examples.json"), "r", encoding="utf-8") as f:
        exemplos = json.load(f)
    return inputs, exemplos


def executar_tecnica(client, tecnica_nome, tarefa, input_texto, exemplos, dry_run=False):
    """
    Monta prompt e envia ao LLM conforme a técnica.
    Retorna dict com resultado e métricas.
    """
    system = ""
    if tecnica_nome == "zero_shot":
        prompt = zero_shot(tarefa, input_texto)
    elif tecnica_nome == "few_shot":
        prompt = few_shot(tarefa, input_texto, exemplos)
    elif tecnica_nome == "chain_of_thought":
        prompt = chain_of_thought(tarefa, input_texto)
    elif tecnica_nome == "role_prompting":
        system, prompt = role_prompting(tarefa, input_texto)
    else:
        raise ValueError(f"Técnica desconhecida: {tecnica_nome}")

    tokens_prompt = contar_tokens(prompt + system)

    if dry_run:
        return {
            "resposta": f"[DRY-RUN] {tecnica_nome} para '{tarefa['nome']}'",
            "tokens_prompt": tokens_prompt,
            "tokens_resposta": 0,
            "tempo_ms": 0,
            "system": system,
        }

    resultado = client.chat(prompt, system=system, temp=0.7)
    resultado["system"] = system
    resultado["prompt"] = prompt
    return resultado


def main():
    parser = argparse.ArgumentParser(description="GameForge AI · Prompt Toolkit")
    parser.add_argument("--tarefa", type=str, default=None, help="Rodar apenas uma tarefa específica.")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem chamar o LLM.")
    args = parser.parse_args()

    print("=" * 60)
    print("  🎮 GameForge AI — Prompt Toolkit")
    print("  Comparação de técnicas de prompting para games")
    print("=" * 60)

    client = LLMClient() if not args.dry_run else None
    inputs_data, exemplos_data = carregar_dados()

    tarefas = TAREFAS
    if args.tarefa:
        tarefas = [get_tarefa(args.tarefa)]

    TECNICAS = ["zero_shot", "few_shot", "chain_of_thought", "role_prompting"]
    resultados = []

    for tarefa in tarefas:
        nome_tarefa = tarefa["nome"]
        inputs_tarefa = inputs_data.get(nome_tarefa, [])
        print(f"\n🔧 Tarefa: {nome_tarefa} ({len(inputs_tarefa)} inputs)")

        for tecnica in TECNICAS:
            print(f"  ├─ Técnica: {tecnica}")
            acuracias = []
            total_tokens_p = 0
            total_tokens_r = 0
            total_tempo = 0

            for item in inputs_tarefa:
                try:
                    res = executar_tecnica(
                        client, tecnica, tarefa,
                        item["input"], exemplos_data,
                        dry_run=args.dry_run,
                    )
                    acuracia = medir_acuracia(res["resposta"], item["esperado"])
                    acuracias.append(acuracia)
                    total_tokens_p += res["tokens_prompt"]
                    total_tokens_r += res["tokens_resposta"]
                    total_tempo += res["tempo_ms"]
                except Exception as e:
                    print(f"     ⚠️  Erro: {e}")
                    acuracias.append(0.0)

            n = len(inputs_tarefa) or 1
            # Consistência: testa no primeiro input
            consistencia = 0.5
            if not args.dry_run and inputs_tarefa:
                try:
                    first_input = inputs_tarefa[0]["input"]
                    if tecnica == "role_prompting":
                        system, prompt = role_prompting(tarefa, first_input)
                    else:
                        prompt = globals()[tecnica](tarefa, first_input) if tecnica != "few_shot" \
                            else few_shot(tarefa, first_input, exemplos_data)
                        system = ""
                    consistencia = medir_consistencia(client, prompt, system=system, n=3)
                except Exception:
                    consistencia = 0.0

            resultados.append({
                "tarefa": nome_tarefa,
                "tecnica": tecnica,
                "acuracia": round(sum(acuracias) / n, 2),
                "consistencia": consistencia,
                "tokens_prompt": round(total_tokens_p / n),
                "tokens_resposta": round(total_tokens_r / n),
                "tempo_ms": round(total_tempo / n),
            })
            print(f"     ✓ acurácia={acuracias}")

    # ── Relatório ──────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  📊 GERANDO RELATÓRIO")
    print("=" * 60)

    df = gerar_tabela(resultados)
    grafico_acuracia(df)
    grafico_custo(df)
    recomendar(df)

    # ── Teste de temperatura (melhor prompt geral) ─────────────────────────
    if not args.dry_run and resultados:
        melhor = max(resultados, key=lambda r: r["acuracia"])
        print(f"\n🌡️  Teste de temperatura para '{melhor['tarefa']}' × '{melhor['tecnica']}'")
        tarefa_obj = get_tarefa(melhor["tarefa"])
        sample_input = inputs_data[melhor["tarefa"]][0]["input"]

        if melhor["tecnica"] == "role_prompting":
            system, prompt = role_prompting(tarefa_obj, sample_input)
        elif melhor["tecnica"] == "few_shot":
            prompt = few_shot(tarefa_obj, sample_input, exemplos_data)
            system = ""
        elif melhor["tecnica"] == "chain_of_thought":
            prompt = chain_of_thought(tarefa_obj, sample_input)
            system = ""
        else:
            prompt = zero_shot(tarefa_obj, sample_input)
            system = ""

        res_temp = testar_temperatura(client, prompt, system=system)
        grafico_temperatura(res_temp)

    print("\n✅ Toolkit concluído. Resultados em output/")


if __name__ == "__main__":
    main()
