"""
prompt_builder.py — Anatomia de prompts (Aula 05)
Princípio: instrução e dados sempre separados.
"""


def montar_prompt(instrucao: str, contexto: str = "", input_dados: str = "", formato_output: str = "") -> str:
    """
    Monta prompt estruturado separando instrução de dados.
    Valida que nenhum componente crítico está vazio.
    """
    if not instrucao.strip():
        raise ValueError("instrucao não pode ser vazia.")
    if not input_dados.strip():
        raise ValueError("input_dados não pode ser vazio.")

    partes = [f"## Instrução\n{instrucao.strip()}"]

    if contexto.strip():
        partes.append(f"## Contexto\n{contexto.strip()}")

    partes.append(f"## Dados de Entrada\n{input_dados.strip()}")

    if formato_output.strip():
        partes.append(f"## Formato de Saída\n{formato_output.strip()}")

    return "\n\n".join(partes)


def adicionar_exemplos(prompt: str, exemplos: list[dict]) -> str:
    """
    Adiciona exemplos few-shot ao prompt.
    Cada exemplo: {"input": "...", "output": "..."}
    """
    if not exemplos:
        return prompt

    bloco = "## Exemplos\n"
    for ex in exemplos:
        bloco += f'Input: "{ex["input"]}"\nOutput: "{ex["output"]}"\n\n'

    # Insere exemplos antes dos Dados de Entrada
    if "## Dados de Entrada" in prompt:
        return prompt.replace("## Dados de Entrada", bloco.strip() + "\n\n## Dados de Entrada", 1)
    return prompt + "\n\n" + bloco.strip()


def adicionar_cot(prompt: str, passos: list[str]) -> str:
    """
    Adiciona instrução de chain-of-thought com passos explícitos.
    """
    if not passos:
        return prompt

    passos_fmt = "\n".join(f"{i+1}. {p}" for i, p in enumerate(passos))
    cot_bloco = f"## Raciocínio Passo a Passo\nAnalise seguindo exatamente esta sequência:\n{passos_fmt}"

    if "## Formato de Saída" in prompt:
        return prompt.replace("## Formato de Saída", cot_bloco + "\n\n## Formato de Saída", 1)
    return prompt + "\n\n" + cot_bloco
