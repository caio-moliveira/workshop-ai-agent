"""
Estado Corrigido para o Sistema de Suporte Multi-Agente
Compatível com create_react_agent
"""

from typing import Dict, Any, TypedDict, List
from datetime import datetime
from enum import Enum
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


# === ENUMS BÁSICOS ===


class CategoryType(str, Enum):
    """Tipos de categoria de consulta"""

    TECHNICAL = "Technical"
    BILLING = "Billing"
    GENERAL = "General"


class SentimentType(str, Enum):
    """Tipos de sentimento"""

    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"


class AgentType(str, Enum):
    """Tipos de agente"""

    COORDENADOR = "Coordenador"
    TECNICO = "Técnico"
    FINANCEIRO = "Financeiro"
    GERAL = "Geral"
    ESCALACAO = "Escalação"


# === ESTADO PRINCIPAL COMPATÍVEL COM create_react_agent ===


class StateSuporteSimples(TypedDict):
    """Estado compatível com create_react_agent e MessagesState"""

    # Campos obrigatórios para create_react_agent
    messages: List[BaseMessage]
    remaining_steps: int

    # Campos customizados para nosso sistema
    query: str
    timestamp: str
    category: CategoryType
    sentiment: SentimentType
    response: str
    agent_used: AgentType
    escalated: bool


# === UTILITÁRIOS ===


def criar_estado_inicial(query: str) -> StateSuporteSimples:
    """Cria estado inicial compatível com create_react_agent"""
    from langchain_core.messages import HumanMessage

    return StateSuporteSimples(
        # Campos obrigatórios para create_react_agent
        messages=[HumanMessage(content=query)],
        remaining_steps=10,  # Número máximo de iterações ReAct
        # Campos customizados
        query=query,
        timestamp=datetime.now().isoformat(),
        category=CategoryType.GENERAL,
        sentiment=SentimentType.NEUTRAL,
        response="",
        agent_used=AgentType.COORDENADOR,
        escalated=False,
    )


def get_resumo_estado(state: StateSuporteSimples) -> Dict[str, Any]:
    """Retorna resumo do estado para logs"""
    return {
        "query": state["query"][:50] + "..."
        if len(state["query"]) > 50
        else state["query"],
        "category": state["category"],
        "sentiment": state["sentiment"],
        "agent_used": state["agent_used"],
        "escalated": state["escalated"],
    }
