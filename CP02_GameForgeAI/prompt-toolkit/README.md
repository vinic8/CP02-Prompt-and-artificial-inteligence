# 🎮 GameForge AI — Prompt Toolkit
**Checkpoint 02 · FIAP · Prompt Engineering & Artificial Intelligence**

Toolkit Python modular que aplica automaticamente 4 técnicas de prompting (Zero-Shot, Few-Shot, Chain-of-Thought e Role Prompting) sobre tarefas reais de uma empresa de videogame, compara resultados e recomenda a melhor abordagem.

---

## Domínio
**GameForge AI** — empresa fictícia de videogame desenvolvendo novos tipos de games e tecnologias imersivas (XR, IA adaptativa, haptics). O toolkit resolve 4 tarefas críticas do negócio:

| Tarefa | Tipo | Descrição |
|--------|------|-----------|
| `classificacao_feedback` | Classificação | Classifica feedback de jogadores em POSITIVO/NEGATIVO/NEUTRO/MISTO |
| `extracao_requisitos` | Extração | Extrai requisitos técnicos de features em JSON estruturado |
| `geracao_pitch` | Geração | Gera pitch executivo para novos conceitos de jogos |
| `sumarizacao_tendencias` | Sumarização | Sumariza relatórios de mercado gamer em bullet points executivos |

---

## Pré-requisitos
- Python 3.10+
- [Ollama](https://ollama.com) instalado e rodando localmente
- Modelo `gpt-oss:120b` baixado no Ollama

```bash
# Instalar e iniciar o Ollama
ollama pull gpt-oss:120b
ollama serve
```

---

## Instalação

```bash
# 1. Clone ou descompacte o projeto
cd prompt-toolkit

# 2. Crie o ambiente virtual
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o ambiente
cp .env.example .env
# Edite .env se necessário (padrão: localhost:11434)
```

---

## Execução

```bash
# Rodar todas as tarefas (requer Ollama ativo)
python main.py

# Rodar apenas uma tarefa específica
python main.py --tarefa classificacao_feedback

# Simular sem chamar o LLM (dry-run para testar estrutura)
python main.py --dry-run
```

---

## Saídas geradas

```
output/
├── resultados.csv          # Tabela comparativa: tarefa × técnica × métricas
└── graficos/
    ├── acuracia.png        # Barras agrupadas: acurácia por técnica × tarefa
    ├── custo_tokens.png    # Tokens médios por técnica
    └── temperatura.png     # Consistência × temperatura (0.1 / 0.5 / 1.0)
```

---

## Estrutura do Projeto

```
prompt-toolkit/
├── README.md
├── requirements.txt
├── .env.example
├── main.py                     # Ponto de entrada
├── src/
│   ├── llm_client.py           # Conexão com Ollama API
│   ├── prompt_builder.py       # Anatomia de prompts (Aula 05)
│   ├── techniques.py           # 4 técnicas: ZS, FS, CoT, Role
│   ├── tasks.py                # 4 tarefas do domínio GameForge
│   ├── evaluator.py            # Métricas: tokens, acurácia, consistência
│   └── report.py               # Tabelas CSV + gráficos matplotlib
├── data/
│   ├── inputs.json             # 5+ inputs reais por tarefa
│   └── examples.json           # Exemplos para few-shot
├── prompts/
│   ├── system_prompts.json     # 4 personas detalhadas (Role Prompting)
│   └── templates.json          # Templates por tarefa
└── output/
    └── graficos/
```

---

## Stack Técnica

| Componente | Tecnologia |
|------------|------------|
| Linguagem | Python 3.10+ |
| LLM | Ollama API — `gpt-oss:120b` |
| Contagem de tokens | tiktoken (cl100k_base) |
| Visualização | matplotlib + pandas |
| Variáveis de ambiente | python-dotenv |
| HTTP | requests |

---

## Guia de Bolso — Quando Usar Cada Técnica

| Técnica | Use quando... | Evite quando... |
|---------|--------------|-----------------|
| **Zero-Shot** | Tarefa simples, formato bem definido, resposta rápida | Tarefa ambígua ou com muitas variações |
| **Few-Shot** | Formato de saída preciso e consistente é crítico | Exemplos são escassos ou de baixa qualidade |
| **Chain-of-Thought** | Raciocínio complexo, extração multi-etapas, diagnóstico | Tarefas simples onde passos extras só adicionam tokens |
| **Role Prompting** | Tom especializado importa, contexto técnico profundo | Tarefas genéricas sem necessidade de expertise específica |
