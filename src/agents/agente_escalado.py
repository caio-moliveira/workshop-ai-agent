"""
Agente de Escalação - Sistema de Suporte Multi-Agente
Gerencia casos que precisam de atenção humana especializada
"""

from typing import Dict, Any
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class AgenteEscalacao:
    """
    Agente responsável por:
    - Escalar casos complexos ou urgentes
    - Categorizar nível de escalação
    - Preparar informações para agentes humanos
    - Acompanhar tempo de resposta
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.1)
        self.escalation_levels = {
            "nivel_1": "Supervisor de atendimento",
            "nivel_2": "Especialista técnico sênior",
            "nivel_3": "Gerente de suporte",
            "nivel_4": "Diretor de operações",
        }

    def determinar_nivel_escalacao(self, state: Dict[str, Any]) -> str:
        """
        Determina o nível apropriado de escalação
        """
        query = state["query"].lower()
        sentiment = state.get("sentiment", "Neutral")
        category = state.get("category", "General")

        # Casos críticos - Nível 4
        if any(
            word in query
            for word in ["processo judicial", "mídia", "vazamento de dados"]
        ):
            return "nivel_4"

        # Casos urgentes - Nível 3
        elif any(word in query for word in ["fraude", "segurança", "dados perdidos"]):
            return "nivel_3"

        # Casos técnicos complexos - Nível 2
        elif category == "Technical" and any(
            word in query for word in ["sistema", "servidor", "banco de dados"]
        ):
            return "nivel_2"

        # Casos gerais com sentimento negativo - Nível 1
        elif sentiment == "Negative":
            return "nivel_1"

        else:
            return "nivel_1"

    def processar_escalacao(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa a escalação e prepara informações para agente humano
        """
        nivel = self.determinar_nivel_escalacao(state)
        responsavel = self.escalation_levels[nivel]

        prompt = ChatPromptTemplate.from_template(
            """
            Você é responsável por preparar escalações para agentes humanos. 
            Crie um resumo claro e objetivo da situação.
            
            Consulta original: {query}
            Categoria: {category}
            Sentimento: {sentiment}
            Prioridade: {priority}
            Nível de escalação: {nivel}
            Responsável: {responsavel}
            
            Prepare um resumo estruturado com:
            1. SITUAÇÃO: Descrição clara do problema
            2. CONTEXTO: Categoria, sentimento e prioridade
            3. AÇÃO REQUERIDA: O que o agente humano deve fazer
            4. URGÊNCIA: Por que precisa de atenção humana
            
            Seja conciso mas complete.
            """
        )

        chain = prompt | self.llm
        resumo_escalacao = chain.invoke(
            {
                "query": state["query"],
                "category": state.get("category", "N/A"),
                "sentiment": state.get("sentiment", "N/A"),
                "priority": state.get("priority", "N/A"),
                "nivel": nivel,
                "responsavel": responsavel,
            }
        ).content

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        escalation_response = f"""
🚨 ESCALAÇÃO NECESSÁRIA 🚨

Timestamp: {timestamp}
Nível: {nivel.upper()}
Responsável: {responsavel}

{resumo_escalacao}

---
Este caso foi automaticamente escalado devido à complexidade ou sentimento negativo detectado.
Tempo limite para resposta: 2 horas para níveis 3-4, 4 horas para níveis 1-2.
        """

        return {
            "response": escalation_response,
            "agent_used": "Agente de Escalação",
            "escalation_level": nivel,
            "responsible": responsavel,
            "escalated": True,
            "timestamp": timestamp,
        }

    def criar_ticket_escalacao(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um ticket estruturado para o sistema de escalação
        """
        nivel = self.determinar_nivel_escalacao(state)

        ticket = {
            "ticket_id": f"ESC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "escalation_level": nivel,
            "responsible_agent": self.escalation_levels[nivel],
            "original_query": state["query"],
            "category": state.get("category", "Unknown"),
            "sentiment": state.get("sentiment", "Unknown"),
            "priority": state.get("priority", "Medium"),
            "status": "PENDING_HUMAN_REVIEW",
            "sla_deadline": self._calculate_sla_deadline(nivel),
        }

        return {"escalation_ticket": ticket}

    def _calculate_sla_deadline(self, nivel: str) -> str:
        """
        Calcula prazo SLA baseado no nível de escalação
        """
        from datetime import timedelta

        sla_hours = {"nivel_1": 4, "nivel_2": 4, "nivel_3": 2, "nivel_4": 1}

        deadline = datetime.now() + timedelta(hours=sla_hours[nivel])
        return deadline.strftime("%Y-%m-%d %H:%M:%S")
