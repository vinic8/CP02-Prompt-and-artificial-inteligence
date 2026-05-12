"""
tasks.py — Tarefas do domínio GameForge AI (Aula 08)
Empresa de videogame desenvolvendo novas tecnologias e tipos de games.
"""

TAREFAS = [

    # ── TAREFA 1: Classificação de Feedback de Jogadores ──────────────────
    {
        "nome": "classificacao_feedback",
        "tipo": "classificacao",
        "instrucao": (
            "Você é analista de UX da GameForge. "
            "Classifique o feedback do jogador como POSITIVO, NEGATIVO, NEUTRO ou MISTO. "
            "Considere aspectos de jogabilidade, tecnologia e experiência."
        ),
        "contexto": "GameForge lança novos tipos de games com tecnologias imersivas (XR, haptics, IA adaptativa).",
        "formato_output": (
            "Responda APENAS no formato:\n"
            "CLASSIFICAÇÃO: <POSITIVO|NEGATIVO|NEUTRO|MISTO>\n"
            "ASPECTO PRINCIPAL: <gameplay|tecnologia|historia|performance|outro>"
        ),
        "exemplos_fewshot": [
            {"input": "Os controles hápticos são revolucionários, sinto cada impacto!", "output": "CLASSIFICAÇÃO: POSITIVO\nASPECTO PRINCIPAL: tecnologia"},
            {"input": "A IA adaptativa torna cada partida única, mas o frame-rate cai muito.", "output": "CLASSIFICAÇÃO: MISTO\nASPECTO PRINCIPAL: performance"},
            {"input": "História mediana, nada que se destaque.", "output": "CLASSIFICAÇÃO: NEUTRO\nASPECTO PRINCIPAL: historia"},
        ],
        "passos_cot": [
            "Identifique todas as menções positivas no texto.",
            "Identifique todas as menções negativas no texto.",
            "Identifique o aspecto central (gameplay, tecnologia, história, performance).",
            "Compare polaridades e determine a classificação dominante.",
            "Responda no formato exigido.",
        ],
        "persona": "analista_ux_games",
    },

    # ── TAREFA 2: Extração de Requisitos de Feature ───────────────────────
    {
        "nome": "extracao_requisitos",
        "tipo": "extracao",
        "instrucao": (
            "Extraia requisitos técnicos e criativos de uma solicitação de nova feature para o jogo. "
            "Retorne um JSON estruturado com os campos especificados."
        ),
        "contexto": "GameForge desenvolve engines proprietárias com XR, IA generativa e física avançada.",
        "formato_output": (
            "Responda APENAS com JSON válido no formato:\n"
            '{"feature": "", "tecnologia": "", "plataforma": "", "prioridade": "alta|media|baixa", "estimativa_semanas": 0}'
        ),
        "exemplos_fewshot": [
            {
                "input": "Quero um sistema de clima dinâmico que afete a física dos projéteis no multiplayer online para PC.",
                "output": '{"feature": "clima dinâmico com física", "tecnologia": "simulação física + rede", "plataforma": "PC", "prioridade": "media", "estimativa_semanas": 8}',
            },
            {
                "input": "Precisamos de NPCs com diálogos gerados por IA em tempo real para o RPG do console.",
                "output": '{"feature": "NPCs com IA generativa", "tecnologia": "LLM on-device", "plataforma": "console", "prioridade": "alta", "estimativa_semanas": 12}',
            },
        ],
        "passos_cot": [
            "Identifique o nome da feature solicitada.",
            "Determine a tecnologia necessária (IA, física, rede, XR, etc.).",
            "Identifique a plataforma-alvo mencionada ou inferida.",
            "Avalie complexidade e defina prioridade (alta/media/baixa).",
            "Estime semanas de desenvolvimento com base na complexidade.",
            "Monte o JSON final.",
        ],
        "persona": "tech_lead_games",
    },

    # ── TAREFA 3: Geração de Pitch de Novo Conceito de Jogo ───────────────
    {
        "nome": "geracao_pitch",
        "tipo": "geracao",
        "instrucao": (
            "Crie um pitch executivo conciso para um novo conceito de jogo ou tecnologia, "
            "adequado para apresentar a investidores e ao board da GameForge."
        ),
        "contexto": "GameForge busca disrupção com XR imersivo, IA adaptativa, haptics e novos modelos de monetização.",
        "formato_output": (
            "Estruture em:\n"
            "TÍTULO: <nome do jogo/tecnologia>\n"
            "GANCHO: <1 frase impactante>\n"
            "PROBLEMA: <dor do mercado>\n"
            "SOLUÇÃO: <como resolve com tecnologia>\n"
            "DIFERENCIAL: <por que a GameForge é única para isso>\n"
            "PROJEÇÃO: <métrica de sucesso em 12 meses>"
        ),
        "exemplos_fewshot": [
            {
                "input": "Jogo de RPG onde a IA cria a história enquanto você joga, sem roteiro fixo.",
                "output": (
                    "TÍTULO: NarrAI Chronicles\n"
                    "GANCHO: O primeiro RPG onde cada partida é única porque a IA escreve ao vivo.\n"
                    "PROBLEMA: Jogadores abandonam RPGs após 20h por repetição de conteúdo.\n"
                    "SOLUÇÃO: Engine de narrativa generativa em tempo real com LLM otimizado on-device.\n"
                    "DIFERENCIAL: Patente pendente em narrative-branching com memória persistente por jogador.\n"
                    "PROJEÇÃO: 500K MAU e 4.2 stars no meta-score em 12 meses."
                ),
            },
        ],
        "passos_cot": [
            "Identifique o gênero e a tecnologia central do conceito.",
            "Mapeie a dor real do mercado gamer que este conceito resolve.",
            "Defina como a tecnologia proposta resolve o problema de forma única.",
            "Identifique o diferencial competitivo da GameForge.",
            "Projete uma métrica de sucesso realista para 12 meses.",
            "Redija o pitch nos campos especificados.",
        ],
        "persona": "game_designer_senior",
    },

    # ── TAREFA 4: Sumarização de Tendências de Mercado ────────────────────
    {
        "nome": "sumarizacao_tendencias",
        "tipo": "sumarizacao",
        "instrucao": (
            "Sumarize o relatório ou artigo de tendências do mercado gamer em bullet points "
            "executivos para o time de produto da GameForge."
        ),
        "contexto": "GameForge monitora tendências em XR, cloud gaming, IA em games e novos modelos de distribuição.",
        "formato_output": (
            "Responda em:\n"
            "RESUMO EXECUTIVO: <2 frases>\n"
            "TENDÊNCIAS-CHAVE:\n- <tendência 1>\n- <tendência 2>\n- <tendência 3>\n"
            "OPORTUNIDADE PARA GAMEFORGE: <1 ação concreta>"
        ),
        "exemplos_fewshot": [
            {
                "input": "Relatório Newzoo 2024: cloud gaming cresce 34% a.a., mobile representa 52% da receita global, XR headsets vendem 18M unidades.",
                "output": (
                    "RESUMO EXECUTIVO: O mercado gamer global acelera em cloud e mobile, enquanto XR ganha tração de hardware. "
                    "Oportunidades de receita recorrente via streaming e conteúdo cross-device são imediatas.\n"
                    "TENDÊNCIAS-CHAVE:\n- Cloud gaming +34% a.a. reduz barreira de hardware\n"
                    "- Mobile domina com 52% da receita global\n- XR com 18M headsets cria base instalada viável\n"
                    "OPORTUNIDADE PARA GAMEFORGE: Lançar versão cloud do título principal em 6 meses."
                ),
            },
        ],
        "passos_cot": [
            "Identifique os dados quantitativos mais relevantes.",
            "Agrupe por categoria (tecnologia, comportamento, receita).",
            "Selecione as 3 tendências com maior impacto para a GameForge.",
            "Derive uma ação concreta e viável.",
            "Redija no formato especificado.",
        ],
        "persona": "analista_mercado_games",
    },
]


def get_tarefa(nome: str) -> dict:
    """Retorna tarefa pelo nome."""
    for t in TAREFAS:
        if t["nome"] == nome:
            return t
    raise ValueError(f"Tarefa '{nome}' não encontrada.")
