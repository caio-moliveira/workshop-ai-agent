"""
Agente Coordenador - Sistema de Suporte Multi-Agente
Responsável por categorizar consultas e analisar sentimento
"""

from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class AgenteCoordenador:
    """
    Agente responsável por:
    - Categorizar consultas do cliente
    - Analisar sentimento
    - Determinar prioridade
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)

    def categorizar_consulta(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Categoriza a consulta do cliente em: Technical, Billing ou General
        """
        prompt = ChatPromptTemplate.from_template(
            """
            Analise a seguinte consulta de cliente e categorize em uma dessas opções:
            - Technical: Problemas técnicos, bugs, funcionalidades
            - Billing: Questões financeiras, cobranças, pagamentos
            - General: Informações gerais, horários, políticas
            
            Consulta: {query}
            
            Responda apenas com uma palavra: Technical, Billing ou General
            """
        )

        chain = prompt | self.llm
        categoria = chain.invoke({"query": state["query"]}).content.strip()

        return {"category": categoria}

    def analisar_sentimento(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analisa o sentimento da consulta: Positive, Neutral ou Negative
        """
        prompt = ChatPromptTemplate.from_template(
            """
            Analise o sentimento da seguinte consulta de cliente:
            
            Consulta: {query}
            
            Classifique como:
            - Positive: Cliente satisfeito, elogiando
            - Neutral: Consulta neutra, apenas pergunta
            - Negative: Cliente insatisfeito, reclamando, frustrado
            
            Responda apenas: Positive, Neutral ou Negative
            """
        )

        chain = prompt | self.llm
        sentimento = chain.invoke({"query": state["query"]}).content.strip()

        return {"sentiment": sentimento}

    def determinar_prioridade(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determina a prioridade baseada na categoria e sentimento
        """
        categoria = state.get("category", "General")
        sentimento = state.get("sentiment", "Neutral")

        # Lógica simples de prioridade
        if sentimento == "Negative":
            prioridade = "High"
        elif categoria == "Technical" and sentimento == "Neutral":
            prioridade = "Medium"
        elif categoria == "Billing":
            prioridade = "Medium"
        else:
            prioridade = "Low"

        return {"priority": prioridade}

    def determinar_rota(self, state: Dict[str, Any]) -> str:
        """
        Determina qual agente deve processar a consulta
        """
        categoria = state.get("category", "General")
        sentimento = state.get("sentiment", "Neutral")

        # Se sentimento negativo, sempre escalar
        if sentimento == "Negative":
            return "escalate"

        # Rotear baseado na categoria
        if categoria == "Technical":
            return "agent_tecnico"
        elif categoria == "Billing":
            return "agent_financeiro"
        else:
            return "agent_geral"
