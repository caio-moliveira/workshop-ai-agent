"""
Estado Simples para o Sistema de Suporte Multi-Agente
Apenas o essencial para demonstração educacional
"""

from typing import Dict, Any, TypedDict
from datetime import datetime
from enum import Enum


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


# === ESTADO PRINCIPAL ===


class StateSuporteSimples(TypedDict):
    """Estado simples para demonstração do sistema multi-agente"""

    # Entrada
    query: str
    timestamp: str

    # Análise do Coordenador
    category: CategoryType
    sentiment: SentimentType

    # Resposta
    response: str
    agent_used: AgentType

    # Controle simples
    escalated: bool


# === UTILITÁRIOS SIMPLES ===
def criar_estado_inicial(query: str) -> StateSuporteSimples:
    """Cria estado inicial com valores padrão"""
    return StateSuporteSimples(
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
