"""
llm_client.py — Conexão com Ollama API (Aula 05)
Domínio: GameForge AI · empresa de videogame
"""
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "gpt-oss:120b")
        self.timeout = int(os.getenv("OLLAMA_TIMEOUT", 120))
        self.max_tokens = int(os.getenv("MAX_TOKENS", 1024))

    def chat(self, prompt: str, system: str = "", temp: float = 0.7, max_tokens: int = None) -> dict:
        """
        Envia prompt ao Ollama e retorna dict com resposta e métricas.
        Retorna: {"resposta", "tokens_prompt", "tokens_resposta", "tempo_ms"}
        """
        max_tokens = max_tokens or self.max_tokens
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temp,
                "num_predict": max_tokens,
            },
        }

        retries = 3
        for attempt in range(retries):
            try:
                inicio = time.time()
                resp = requests.post(
                    f"{self.host}/api/chat",
                    json=payload,
                    timeout=self.timeout,
                )
                tempo_ms = int((time.time() - inicio) * 1000)
                resp.raise_for_status()
                data = resp.json()

                resposta = data.get("message", {}).get("content", "")
                tokens_prompt = data.get("prompt_eval_count", 0)
                tokens_resposta = data.get("eval_count", 0)

                return {
                    "resposta": resposta,
                    "tokens_prompt": tokens_prompt,
                    "tokens_resposta": tokens_resposta,
                    "tempo_ms": tempo_ms,
                }

            except requests.exceptions.Timeout:
                if attempt == retries - 1:
                    raise RuntimeError(f"Timeout após {retries} tentativas.")
                time.sleep(2 ** attempt)

            except requests.exceptions.ConnectionError:
                raise RuntimeError(
                    f"Não foi possível conectar ao Ollama em {self.host}. "
                    "Certifique-se de que o Ollama está rodando."
                )

            except requests.exceptions.HTTPError as e:
                if resp.status_code == 429:
                    time.sleep(5)
                    continue
                raise RuntimeError(f"Erro HTTP {resp.status_code}: {e}")
