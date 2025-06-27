"""
Workflow de Suporte Multi-Agente usando LangGraph
Versão simplificada e estável para fins educacionais
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
)
from agents.agente_coordenador import categorizar_consulta, analisar_sentimento
from agents.agente_tecnico import buscar_solucao_tecnica, avaliar_complexidade_tecnica
from agents.agente_financeiro import consultar_politica_financeira, calcular_reembolso
from agents.agente_geral import buscar_informacao_empresa


class WorkflowSuporteMultiAgente:
    """Workflow principal usando tools diretamente - versão educacional simplificada"""

    def __init__(self):
        # Criar workflow
        self.app = self._criar_workflow()

    def _criar_workflow(self) -> StateGraph:
        """Cria workflow simplificado usando tools diretamente"""
        workflow = StateGraph(StateSuporteSimples)

        # === NÓSAÇÕES ===
        workflow.add_node("inicializar", self._inicializar)
        workflow.add_node("categorizar", self._categorizar)
        workflow.add_node("analisar_sentimento", self._analisar_sentimento)
        workflow.add_node("agent_tecnico", self._processar_tecnico)
        workflow.add_node("agent_financeiro", self._processar_financeiro)
        workflow.add_node("agent_geral", self._processar_geral)

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
            },
        )

        # Todos vão para o fim
        workflow.add_edge("agent_tecnico", END)
        workflow.add_edge("agent_financeiro", END)
        workflow.add_edge("agent_geral", END)

        # Ponto de entrada
        workflow.set_entry_point("inicializar")

        return workflow.compile()

    # === FUNÇÕES DOS NÓS ===

    def _inicializar(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Inicializa estado com timestamp"""
        print("🚀 Inicializando processamento...")
        return {**state, "timestamp": datetime.now().isoformat()}

    def _categorizar(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Categoriza consulta usando tool de categorização diretamente"""
        print("🎯 Categorizando consulta...")

        # Usar tool de categorização diretamente
        query = state["query"]
        categoria = categorizar_consulta.invoke({"query": query})

        print(f"📂 Categoria identificada: {categoria}")
        return {**state, "category": categoria}

    def _analisar_sentimento(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Analisa sentimento usando tool de sentimento diretamente"""
        print("😊 Analisando sentimento...")

        # Usar tool de sentimento diretamente
        query = state["query"]
        sentimento = analisar_sentimento.invoke({"query": query})

        print(f"💭 Sentimento detectado: {sentimento}")
        return {**state, "sentiment": sentimento}

    def _processar_tecnico(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Processa com ferramentas técnicas diretamente"""
        print("🔧 Processando com Agente Técnico...")

        query = state["query"]

        # Usar tools técnicas diretamente
        solucao = buscar_solucao_tecnica.invoke({"problema": query})
        complexidade = avaliar_complexidade_tecnica.invoke({"query": query})

        # Criar resposta baseada nas tools
        if complexidade == "escalate":
            resposta = f"⚠️ Este problema será escalado para um especialista de nível 2.\n\n{solucao}"
            escalado = True
        else:
            resposta = f"🔧 Solução técnica encontrada:\n\n{solucao}"
            escalado = False

        print("✅ Solução técnica gerada")
        return {
            **state,
            "response": resposta,
            "agent_used": AgentType.TECNICO,
            "escalated": escalado,
        }

    def _processar_financeiro(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Processa com ferramentas financeiras diretamente"""
        print("💰 Processando com Agente Financeiro...")

        query = state["query"]

        # Usar tools financeiras diretamente
        if "reembolso" in query.lower() or "estorno" in query.lower():
            politica = consultar_politica_financeira.invoke(
                {"tipo_consulta": "reembolso"}
            )
            resposta = f"💰 Política de Reembolso:\n\n{politica}\n\nSe precisar calcular um valor específico, por favor informe o valor da compra e há quantos dias foi realizada."
        elif "pagamento" in query.lower():
            politica = consultar_politica_financeira.invoke(
                {"tipo_consulta": "pagamento"}
            )
            resposta = f"💳 Formas de Pagamento:\n\n{politica}"
        else:
            # Consulta geral financeira
            politica = consultar_politica_financeira.invoke({"tipo_consulta": query})
            resposta = f"💰 Informação Financeira:\n\n{politica}"

        print("✅ Resposta financeira gerada")
        return {
            **state,
            "response": resposta,
            "agent_used": AgentType.FINANCEIRO,
            "escalated": False,
        }

    def _processar_geral(self, state: StateSuporteSimples) -> StateSuporteSimples:
        """Processa com ferramentas gerais diretamente"""
        print("ℹ️ Processando com Agente Geral...")

        query = state["query"]

        # Usar tool geral diretamente
        informacao = buscar_informacao_empresa.invoke({"tipo_info": query})
        resposta = f"ℹ️ Informação da Empresa:\n\n{informacao}"

        print("✅ Informações gerais fornecidas")
        return {
            **state,
            "response": resposta,
            "agent_used": AgentType.GERAL,
            "escalated": False,
        }

    def _rotear_agente(self, state: StateSuporteSimples) -> str:
        """Determina qual agente deve processar a consulta"""

        # Rotear por categoria
        category = state.get("category", CategoryType.GENERAL)
        sentiment = state.get("sentiment", "Neutral")

        print(
            f"🎯 Roteando baseado em - Categoria: {category}, Sentimento: {sentiment}"
        )

        if sentiment == "Negative":
            print("⚠️ Sentimento negativo detectado - processando com atenção especial")

        # Roteamento baseado na categoria
        if category == "Technical":
            return "agent_tecnico"
        elif category == "Billing":
            return "agent_financeiro"
        else:
            return "agent_geral"

    # === INTERFACE PÚBLICA ===

    def processar_consulta(self, query: str) -> Dict[str, Any]:
        """
        Interface principal para processar uma consulta
        Versão simplificada usando tools diretamente
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
    Versão simplificada e estável
    """
    print("🔧 Criando workflow multi-agente refatorado...")
    workflow = WorkflowSuporteMultiAgente()
    print("✅ Workflow criado com agentes refatorados!")

    # Gerar visualização do grafo
    try:
        print("📊 Gerando visualização do workflow...")
        graph_image = workflow.app.get_graph().draw_mermaid_png()

        # Salvar na pasta graph
        with open("src/graph/workflow_diagram.png", "wb") as f:
            f.write(graph_image)
        print("✅ Diagrama salvo em: src/graph/workflow_diagram.png")

    except Exception as e:
        print(f"⚠️ Erro ao gerar diagrama: {e}")

    return workflow
