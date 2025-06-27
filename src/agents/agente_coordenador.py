from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from utils.state import StateSuporteSimples
from memory.workflow_memory import checkpointer as default_checkpointer, in_memory_store

# --- Definição das Ferramentas (Tools) ---


@tool
def categorizar_consulta(query: str) -> str:
    """
    Categoriza a consulta do cliente em: Technical, Billing ou General.

    Args:
        query: A consulta do cliente.

    Returns:
        str: Uma das categorias: Technical, Billing ou General.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        """
        Analise a seguinte consulta de cliente e categorize em uma dessas opções:
        - Technical: Problemas técnicos, bugs, funcionalidades.
        - Billing: Questões financeiras, cobranças, pagamentos.
        - General: Informações gerais, horários, políticas.
        
        Consulta: {query}
        
        Responda apenas com uma palavra: Technical, Billing ou General
        """
    )
    chain = prompt | llm
    return chain.invoke({"query": query}).content.strip()


@tool
def analisar_sentimento(query: str) -> str:
    """
    Analisa o sentimento da consulta do cliente: Positive, Neutral ou Negative.

    Args:
        query: A consulta do cliente.

    Returns:
        str: Positive, Neutral ou Negative.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        """
        Analise o sentimento da seguinte consulta de cliente:
        
        Consulta: {query}
        
        Classifique como:
        - Positive: Cliente satisfeito, elogiando.
        - Neutral: Consulta neutra, apenas pergunta.
        - Negative: Cliente insatisfeito, reclamando, frustrado.
        
        Responda apenas: Positive, Neutral ou Negative
        """
    )
    chain = prompt | llm
    return chain.invoke({"query": query}).content.strip()


@tool
def determinar_prioridade(categoria: str, sentimento: str) -> str:
    """
    Determina a prioridade (High, Medium, Low) com base na categoria e sentimento.

    Args:
        categoria: A categoria da consulta (Technical, Billing, General).
        sentimento: O sentimento da consulta (Positive, Neutral, Negative).

    Returns:
        str: A prioridade: High, Medium ou Low.
    """
    if sentimento == "Negative":
        return "High"
    if categoria == "Billing":
        return "Medium"
    if categoria == "Technical" and sentimento == "Neutral":
        return "Medium"
    return "Low"


@tool
def determinar_rota(categoria: str, sentimento: str) -> str:
    """
    Determina para qual agente a consulta deve ser encaminhada.

    Args:
        categoria: A categoria da consulta (Technical, Billing, General).
        sentimento: O sentimento da consulta (Positive, Neutral, Negative).

    Returns:
        str: A rota: escalate, agent_tecnico, agent_financeiro ou agent_geral.
    """
    if sentimento == "Negative":
        return "escalate"
    if categoria == "Technical":
        return "agent_tecnico"
    if categoria == "Billing":
        return "agent_financeiro"
    return "agent_geral"


# --- Lista de Tools do Coordenador ---
coordenador_tools = [
    categorizar_consulta,
    analisar_sentimento,
    determinar_prioridade,
    determinar_rota,
]

# --- Prompt do Sistema ---
coordenador_prompt = """
Você é um Agente Coordenador de Suporte ao Cliente altamente eficiente.

Sua função é analisar as consultas dos clientes e executar as seguintes tarefas, estritamente nesta ordem:
1. Primeiro, use a ferramenta `categorizar_consulta` para definir a categoria da consulta (Technical, Billing ou General).
2. Depois, use a ferramenta `analisar_sentimento` para identificar o sentimento (Positive, Neutral ou Negative).
3. Com a categoria e o sentimento em mãos, use a ferramenta `determinar_prioridade` para definir a prioridade (High, Medium, Low).
4. Finalmente, use a ferramenta `determinar_rota` para decidir qual o próximo agente ou ação (escalate, agent_tecnico, agent_financeiro, agent_geral).

Ao final do processo, apresente um resumo claro e conciso de todas as análises realizadas (Categoria, Sentimento, Prioridade e Rota).

Você tem acesso às seguintes ferramentas:
- categorizar_consulta: Categoriza a consulta em Technical, Billing ou General
- analisar_sentimento: Analisa o sentimento em Positive, Neutral ou Negative  
- determinar_prioridade: Determina prioridade baseada na categoria e sentimento
- determinar_rota: Determina qual agente deve processar a consulta

CORE RESPONSIBILITIES:
- Analisar e categorizar consultas de clientes
- Determinar sentimento e prioridade
- Rotear para o agente apropriado
- Sempre manter um tom profissional e eficiente
"""


# --- Classe do Agente Coordenador ---
class AgenteCoordenador:
    """
    Agente Coordenador usando create_react_agent - versão minimalista.
    """

    def __init__(self):
        self.agent = create_react_agent(
            model=ChatOpenAI(model="gpt-4o-mini"),
            tools=coordenador_tools,
            prompt=coordenador_prompt,
            state_schema=StateSuporteSimples,
            checkpointer=default_checkpointer,
            store=in_memory_store,
        )
