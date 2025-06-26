"""
Agente Técnico - Sistema de Suporte Multi-Agente
Especializado em resolver problemas técnicos
Conectado a MCP para buscar soluções online
"""

from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class AgenteTecnico:
    """
    Agente especializado em suporte técnico:
    - Resolve problemas técnicos
    - Busca soluções em documentação (via MCP)
    - Fornece instruções passo-a-passo
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.3)
        self.knowledge_base = {
            "login": "Verifique suas credenciais e tente redefinir a senha",
            "conexao": "Verifique sua conexão com a internet e tente novamente",
            "erro": "Tente limpar o cache do navegador e recarregar a página",
            "lentidao": "Verifique se há outros programas consumindo recursos",
        }

    def buscar_solucao_mcp(self, problema: str) -> str:
        """
        Simula busca via MCP (Model Context Protocol)
        Em implementação real, conectaria com servidor MCP de web search
        """
        # Simulação de busca MCP
        problema_lower = problema.lower()

        for keyword, solucao in self.knowledge_base.items():
            if keyword in problema_lower:
                return f"[MCP Search] Encontrei: {solucao}"

        return (
            "[MCP Search] Nenhuma solução específica encontrada na base de conhecimento"
        )

    def processar_consulta_tecnica(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa consultas técnicas e fornece soluções
        """
        query = state["query"]

        # Busca solução via MCP
        solucao_mcp = self.buscar_solucao_mcp(query)

        prompt = ChatPromptTemplate.from_template(
            """
            Você é um especialista em suporte técnico. Analise a consulta do cliente e forneça uma solução clara e prática.
            
            Consulta do cliente: {query}
            
            Informações da base de conhecimento: {mcp_info}
            
            Forneça uma resposta estruturada com:
            1. Diagnóstico do problema
            2. Solução passo-a-passo
            3. Informações adicionais se necessário
            
            Seja claro, objetivo e técnico, mas acessível.
            """
        )

        chain = prompt | self.llm
        resposta = chain.invoke({"query": query, "mcp_info": solucao_mcp}).content

        return {
            "response": resposta,
            "agent_used": "Agente Técnico",
            "mcp_consulted": True,
        }

    def avaliar_complexidade(self, state: Dict[str, Any]) -> str:
        """
        Avalia se o problema requer escalação
        """
        query = state["query"].lower()

        # Palavras que indicam alta complexidade
        palavras_complexas = [
            "sistema travou",
            "erro crítico",
            "dados perdidos",
            "não funciona nada",
            "servidor",
            "banco de dados",
        ]

        for palavra in palavras_complexas:
            if palavra in query:
                return "escalate"

        return "continue"
