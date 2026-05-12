"""
techniques.py — 4 técnicas de prompting (Aulas 06 + 07)
Cada função recebe tarefa + input e retorna prompt(s) montado(s).
"""
import json
import os
from src.prompt_builder import montar_prompt, adicionar_exemplos, adicionar_cot

_SYSTEM_PROMPTS_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "system_prompts.json")


def _load_system_prompts() -> dict:
    with open(_SYSTEM_PROMPTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ── 1. ZERO-SHOT ────────────────────────────────────────────────────────────
def zero_shot(tarefa: dict, input_texto: str) -> str:
    """
    Monta prompt direto sem exemplos. Instrução clara + formato definido.
    """
    return montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )


# ── 2. FEW-SHOT ─────────────────────────────────────────────────────────────
def few_shot(tarefa: dict, input_texto: str, exemplos: list[dict]) -> str:
    """
    Monta prompt com 2–3 exemplos no formato Input: "..." → Output: "...".
    """
    prompt_base = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )
    exemplos_tarefa = exemplos.get(tarefa["nome"], tarefa.get("exemplos_fewshot", []))[:3]
    return adicionar_exemplos(prompt_base, exemplos_tarefa)


# ── 3. CHAIN-OF-THOUGHT ──────────────────────────────────────────────────────
def chain_of_thought(tarefa: dict, input_texto: str) -> str:
    """
    Monta prompt com raciocínio explícito passo a passo.
    """
    prompt_base = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )
    passos = tarefa.get("passos_cot", [])
    return adicionar_cot(prompt_base, passos)


# ── 4. ROLE PROMPTING ────────────────────────────────────────────────────────
def role_prompting(tarefa: dict, input_texto: str) -> tuple[str, str]:
    """
    Usa system prompt com persona detalhada do system_prompts.json.
    Retorna tupla (system_prompt, user_prompt).
    """
    personas = _load_system_prompts()
    persona_key = tarefa.get("persona", "game_designer")
    persona = personas.get(persona_key, personas.get("game_designer"))

    system_prompt = (
        f"Você é {persona['nome']}.\n"
        f"Experiência: {persona['experiencia']}\n"
        f"Especialidade: {persona['especialidade']}\n"
        f"Tom de voz: {persona['tom_de_voz']}\n"
        f"Limitações: {persona['limitacoes']}"
    )

    user_prompt = montar_prompt(
        instrucao=tarefa["instrucao"],
        contexto=tarefa.get("contexto", ""),
        input_dados=input_texto,
        formato_output=tarefa["formato_output"],
    )

    return system_prompt, user_prompt
