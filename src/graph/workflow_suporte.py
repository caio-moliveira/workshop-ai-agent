"""
Workflow de Suporte Multi-Agente usando LangGraph
Adaptado para funcionar com a estrutura do projeto
"""

from typing import Dict, Any
from langgraph.graph import StateGraph, END
from datetime import datetime

# Imports dos agentes e estado
from utils.state import (
    StateSuporteSimples,
    CategoryType,
    AgentType,
    criar_estado_inicial,
    deve_escalar,
)
from agents.agente_coordenador import AgenteCoordenador
from agents.agente_tecnico import AgenteTecnico
from agents.agente_financeiro import AgenteFinanceiro
from agents.agente_geral import AgenteGeral
from agents.agente_escalado import AgenteEscalacao
from langsmith import traceable


class WorkflowSuporteMultiAgente:
    """Workflow principal que coordena todos os agentes"""

    def __init__(self):
        # Inicializar agentes
        self.coordenador = AgenteCoordenador()
        self.agente_tecnico = AgenteTecnico()
        self.agente_financeiro = AgenteFinanceiro()
        self.agente_geral = AgenteGeral()
        self.agente_escalacao = AgenteEscalacao()

        # Criar workflow
        self.app = self._criar_workflow()

    def _criar_workflow(self) -> StateGraph:
        """Cria workflow simples e direto"""
        workflow = StateGraph(StateSuporteSimples)

        # === NÓSAÇÕES ===
        workflow.add_node("inicializar", self._inicializar)
        workflow.add_node("categorizar", self._categorizar)
        workflow.add_node("analisar_sentimento", self._analisar_sentimento)
        workflow.add_node("agent_tecnico", self._processar_tecnico)
        workflow.add_node("agent_financeiro", self._processar_financeiro)
        workflow.add_node("agent_geral", self._processar_geral)
        workflow.add_node("escalacao", self._processar_escalacao)

        # === EDGES ===
        workflow.add_edge("inicializar", "categorizar")
        workflow.add_edge("categorizar", "analisar_sentimento")

        # Roteamento direto após análise
        workflow.add_conditional_edges(
            "analisar_sentimento",
            self._rotear_agente,
            {
                "agent_tecnico": "agent_tecnico",
                "agent_financeiro": "agent_financeiro",
                "agent_geral": "agent_geral",
                "escalacao": "escalacao",
            },
        )

        # Todos vão para o fim
        workflow.add_edge("agent_tecnico", END)
        workflow.add_edge("agent_financeiro", END)
        workflow.add_edge("agent_geral", END)
        workflow.add_edge("escalacao", END)

        # Ponto de entrada
        workflow.set_entry_point("inicializar")

        return workflow.compile()

    # === FUNÇÕES DOS NÓS ===

    def _inicializar(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Inicializa estado com timestamp"""
        print("🚀 Inicializando processamento...")
        return {**state, "timestamp": datetime.now().isoformat()}

    @traceable(name="Coordenador_Categorizar", tags=["coordenador", "analise"])
    def _categorizar(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Categoriza consulta usando o Coordenador"""
        print("🎯 Categorizando consulta...")
        resultado = self.coordenador.categorizar_consulta(state)
        print(f"📂 Categoria identificada: {resultado.get('category', 'Unknown')}")
        return {**state, **resultado}

    @traceable(name="Coordenador_Sentimento", tags=["coordenador", "analise"])
    def _analisar_sentimento(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Analisa sentimento usando o Coordenador"""
        print("😊 Analisando sentimento...")
        resultado = self.coordenador.analisar_sentimento(state)
        print(f"💭 Sentimento detectado: {resultado.get('sentiment', 'Unknown')}")
        return {**state, **resultado}

    @traceable(name="Agente_Tecnico", tags=["tecnico", "resolucao"])
    def _processar_tecnico(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Processa com Agente Técnico"""
        print("🔧 Processando com Agente Técnico...")
        resultado = self.agente_tecnico.processar_consulta_tecnica(state)
        print("✅ Solução técnica gerada")
        return {**state, **resultado, "agent_used": AgentType.TECNICO}

    @traceable(name="Agente_Financeiro", tags=["financeiro", "cobranca"])
    def _processar_financeiro(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Processa com Agente Financeiro"""
        print("💰 Processando com Agente Financeiro...")
        resultado = self.agente_financeiro.processar_consulta_financeira(state)
        print("✅ Resposta financeira gerada")
        return {**state, **resultado, "agent_used": AgentType.FINANCEIRO}

    @traceable(name="Agente_Geral", tags=["geral", "informacoes"])
    def _processar_geral(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Processa com Agente Geral"""
        print("ℹ️ Processando com Agente Geral...")
        resultado = self.agente_geral.processar_consulta_geral(state)
        print("✅ Informações gerais fornecidas")
        return {**state, **resultado, "agent_used": AgentType.GERAL}

    @traceable(name="Agente_Escalacao", tags=["escalacao", "urgente"])
    def _processar_escalacao(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Processa escalação"""
        print("🚨 Escalando para agente humano...")
        resultado = self.agente_escalacao.processar_escalacao(state)
        print("✅ Escalação processada")
        return {
            **state,
            **resultado,
            "agent_used": AgentType.ESCALACAO,
            "escalated": True,
        }

    # === ROTEAMENTO ===

    def _rotear_agente(self, state: StateSuporteSimples) -> str:
        """Determina qual agente deve processar a consulta"""
        # Se sentimento negativo, escalar
        if deve_escalar(state):
            print(" Sentimento negativo detectado - roteando para escalação")
            return "escalacao"

        # Rotear por categoria
        category = state.get("category", CategoryType.GENERAL)
        print(f"🎯 Roteando para agente baseado na categoria: {category}")

        if category == CategoryType.TECHNICAL:
            return "agent_tecnico"
        elif category == CategoryType.BILLING:
            return "agent_financeiro"
        else:
            return "agent_geral"

    # === INTERFACE PÚBLICA ===

    @traceable(name="Workflow_MultiAgente", tags=["workflow", "orquestracao"])
    def processar_consulta(self, query: str) -> Dict[str, Any]:
        """
        Interface principal para processar uma consulta
        """
        print(f"\n🎯 Processando consulta: '{query[:50]}...'")

        # Estado inicial
        initial_state = criar_estado_inicial(query)

        # Executar workflow
        result = self.app.invoke(initial_state)

        print(f"🎉 Processamento concluído por: {result['agent_used']}")

        # Retornar resultado limpo
        return {
            "query": result["query"],
            "category": result["category"],
            "sentiment": result["sentiment"],
            "response": result["response"],
            "agent_used": result["agent_used"],
            "escalated": result["escalated"],
            "timestamp": result["timestamp"],
        }


# === FUNÇÃO HELPER ===


def criar_workflow() -> WorkflowSuporteMultiAgente:
    """
    Função helper para criar e configurar o workflow
    Compatível com o main.py
    """
    print("🔧 Criando workflow multi-agente...")
    workflow = WorkflowSuporteMultiAgente()
    print("✅ Workflow criado com sucesso!")
    return workflow


# === TESTE STANDALONE ===

if __name__ == "__main__":
    # Teste rápido do workflow
    print("🧪 TESTE DO WORKFLOW")

    workflow = criar_workflow()

    # Teste simples
    resultado = workflow.processar_consulta("Não consigo fazer login")

    print("\nResultado do teste:")
    print(f"Categoria: {resultado['category']}")
    print(f"Sentimento: {resultado['sentiment']}")
    print(f"Agente: {resultado['agent_used']}")
    print(f"Resposta: {resultado['response'][:100]}...")
