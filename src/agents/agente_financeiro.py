"""
Agente Financeiro - Sistema de Suporte Multi-Agente
Especializado em questões de cobrança e pagamentos
"""

from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class AgenteFinanceiro:
    """
    Agente especializado em suporte financeiro:
    - Questões de cobrança
    - Problemas de pagamento
    - Reembolsos e ajustes
    - Informações de fatura
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        # Simulação de dados financeiros
        self.sistema_financeiro = {
            "politica_reembolso": "30 dias para produtos digitais, 60 dias para físicos",
            "formas_pagamento": "Cartão, PIX, Boleto, PayPal",
            "prazo_processamento": "2-3 dias úteis para estornos",
        }

    def consultar_sistema_financeiro(self, tipo_consulta: str) -> str:
        """
        Simula consulta ao sistema financeiro interno
        """
        consulta_lower = tipo_consulta.lower()

        if "reembolso" in consulta_lower or "estorno" in consulta_lower:
            return f"Política: {self.sistema_financeiro['politica_reembolso']}"
        elif "pagamento" in consulta_lower:
            return f"Formas aceitas: {self.sistema_financeiro['formas_pagamento']}"
        elif "prazo" in consulta_lower:
            return f"Processamento: {self.sistema_financeiro['prazo_processamento']}"
        else:
            return "Consulta geral ao sistema financeiro"

    def processar_consulta_financeira(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa consultas relacionadas a billing e pagamentos
        """
        query = state["query"]

        # Consulta sistema financeiro
        info_sistema = self.consultar_sistema_financeiro(query)

        prompt = ChatPromptTemplate.from_template(
            """
            Você é um especialista em suporte financeiro e cobrança. Analise a consulta do cliente e forneça uma resposta precisa.
            
            Consulta do cliente: {query}
            
            Informações do sistema: {sistema_info}
            
            Forneça uma resposta que inclua:
            1. Entendimento da situação financeira
            2. Solução ou orientação clara
            3. Próximos passos se necessário
            4. Informações sobre prazos e processos
            
            Seja empático, claro e sempre mencione políticas relevantes.
            """
        )

        chain = prompt | self.llm
        resposta = chain.invoke({"query": query, "sistema_info": info_sistema}).content

        return {
            "response": resposta,
            "agent_used": "Agente Financeiro",
            "system_consulted": True,
        }

    def calcular_reembolso(
        self, valor: float, dias_desde_compra: int
    ) -> Dict[str, Any]:
        """
        Calcula valor de reembolso baseado em políticas
        """
        if dias_desde_compra <= 30:
            percentual = 100
        elif dias_desde_compra <= 60:
            percentual = 50
        else:
            percentual = 0

        valor_reembolso = valor * (percentual / 100)

        return {
            "valor_original": valor,
            "dias_desde_compra": dias_desde_compra,
            "percentual_reembolso": percentual,
            "valor_reembolso": valor_reembolso,
            "elegivel": percentual > 0,
        }

    def verificar_urgencia_financeira(self, state: Dict[str, Any]) -> str:
        """
        Verifica se questão financeira requer atenção urgente
        """
        query = state["query"].lower()

        # Palavras que indicam urgência financeira
        palavras_urgentes = [
            "cobrança indevida",
            "fraude",
            "cartão clonado",
            "valor errado",
            "duplicata",
            "urgente",
        ]

        for palavra in palavras_urgentes:
            if palavra in query:
                return "escalate"

        return "continue"
