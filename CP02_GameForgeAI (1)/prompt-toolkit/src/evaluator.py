"""
evaluator.py — Métricas de qualidade, tokens e consistência
"""
import time
from src.llm_client import LLMClient

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
    _USE_TIKTOKEN = True
except ImportError:
    _USE_TIKTOKEN = False


def contar_tokens(texto: str) -> int:
    """Conta tokens via tiktoken se disponível, senão aproxima (1 token ≈ 0.75 palavras)."""
    if _USE_TIKTOKEN:
        return len(_ENC.encode(texto))
    return max(1, len(texto.split()) * 4 // 3)


def medir_acuracia(resposta: str, esperado) -> float:
    """
    Match exato (str) ou por keywords (dict/list).
    Retorna 0.0 a 1.0.
    """
    resposta_lower = resposta.strip().lower()

    if isinstance(esperado, str):
        return 1.0 if esperado.lower() in resposta_lower else 0.0

    if isinstance(esperado, dict):
        hits = sum(
            1 for v in esperado.values()
            if str(v).lower() in resposta_lower
        )
        return round(hits / len(esperado), 2) if esperado else 0.0

    if isinstance(esperado, list):
        hits = sum(1 for kw in esperado if kw.lower() in resposta_lower)
        return round(hits / len(esperado), 2) if esperado else 0.0

    return 0.0


def medir_consistencia(client: LLMClient, prompt: str, system: str = "", n: int = 3, temp: float = 0.7) -> float:
    """
    Envia o mesmo prompt N vezes e mede % de respostas idênticas.
    Retorna 0.0 a 1.0.
    """
    respostas = []
    for _ in range(n):
        resultado = client.chat(prompt, system=system, temp=temp)
        respostas.append(resultado["resposta"].strip().lower())

    if not respostas:
        return 0.0

    moda = max(set(respostas), key=respostas.count)
    return round(respostas.count(moda) / len(respostas), 2)


def testar_temperatura(client: LLMClient, prompt: str, system: str = "", temps: list[float] = None) -> list[dict]:
    """
    Roda o prompt com diferentes temperaturas (0.1, 0.5, 1.0).
    Retorna lista de dicts com temp, resposta, tokens e consistência.
    """
    if temps is None:
        temps = [0.1, 0.5, 1.0]

    resultados = []
    for temp in temps:
        resultado = client.chat(prompt, system=system, temp=temp)
        consistencia = medir_consistencia(client, prompt, system=system, n=3, temp=temp)
        resultados.append({
            "temperatura": temp,
            "resposta": resultado["resposta"],
            "tokens_prompt": resultado["tokens_prompt"],
            "tokens_resposta": resultado["tokens_resposta"],
            "tempo_ms": resultado["tempo_ms"],
            "consistencia": consistencia,
        })

    return resultados
