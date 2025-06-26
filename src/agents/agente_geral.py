"""
Agente Geral - Sistema de Suporte Multi-Agente
Especializado em atendimento geral e informações da empresa
"""

from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class AgenteGeral:
    """
    Agente especializado em atendimento geral:
    - Informações sobre a empresa
    - Horários de funcionamento
    - Políticas gerais
    - Dúvidas sobre produtos/serviços
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.4)
        # Base de conhecimento da empresa
        self.info_empresa = {
            "horario_funcionamento": "Segunda a Sexta: 8h às 18h, Sábado: 9h às 14h",
            "telefone": "(11) 1234-5678",
            "email": "suporte@empresa.com",
            "endereco": "Rua Exemplo, 123 - São Paulo, SP",
            "politica_privacidade": "Disponível em nosso site na seção legal",
            "garantia": "12 meses para produtos físicos, 30 dias para digitais",
            "entrega": "5-10 dias úteis para todo o Brasil",
        }

    def buscar_informacao_empresa(self, tipo_info: str) -> str:
        """
        Busca informações específicas da empresa
        """
        info_lower = tipo_info.lower()

        if "horario" in info_lower or "funcionamento" in info_lower:
            return self.info_empresa["horario_funcionamento"]
        elif "telefone" in info_lower or "contato" in info_lower:
            return f"Telefone: {self.info_empresa['telefone']}, Email: {self.info_empresa['email']}"
        elif "endereco" in info_lower or "endereço" in info_lower:
            return self.info_empresa["endereco"]
        elif "garantia" in info_lower:
            return self.info_empresa["garantia"]
        elif "entrega" in info_lower or "prazo" in info_lower:
            return self.info_empresa["entrega"]
        else:
            return "Informação geral da empresa disponível"

    def processar_consulta_geral(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa consultas gerais sobre a empresa
        """
        query = state["query"]

        # Busca informação relevante
        info_empresa = self.buscar_informacao_empresa(query)

        prompt = ChatPromptTemplate.from_template(
            """
            Você é um atendente especializado em informações gerais da empresa. Seja cordial, prestativo e informativo.
            
            Consulta do cliente: {query}
            
            Informações da empresa: {empresa_info}
            
            Forneça uma resposta que:
            1. Responda diretamente à pergunta
            2. Inclua informações relevantes da empresa
            3. Seja cordial e profissional
            4. Ofereça ajuda adicional se necessário
            
            Mantenha um tom amigável e prestativo.
            """
        )

        chain = prompt | self.llm
        resposta = chain.invoke({"query": query, "empresa_info": info_empresa}).content

        return {
            "response": resposta,
            "agent_used": "Agente Geral",
            "info_type": "general",
        }

    def identificar_tipo_informacao(self, query: str) -> str:
        """
        Identifica que tipo de informação o cliente está buscando
        """
        query_lower = query.lower()

        if any(
            word in query_lower
            for word in ["horario", "funcionamento", "aberto", "fechado"]
        ):
            return "horarios"
        elif any(
            word in query_lower for word in ["contato", "telefone", "email", "falar"]
        ):
            return "contato"
        elif any(
            word in query_lower
            for word in ["endereco", "endereço", "localização", "onde"]
        ):
            return "endereco"
        elif any(
            word in query_lower for word in ["produto", "serviço", "oferece", "vende"]
        ):
            return "produtos"
        elif any(
            word in query_lower
            for word in ["politica", "política", "termos", "privacidade"]
        ):
            return "politicas"
        else:
            return "geral"

    def sugerir_outras_informacoes(self, state: Dict[str, Any]) -> Dict[str, str]:
        """
        Sugere outras informações que podem ser úteis
        """
        sugestoes = {
            "horarios": "Horários de funcionamento",
            "contato": "Formas de contato",
            "produtos": "Informações sobre produtos",
            "garantia": "Políticas de garantia",
            "entrega": "Prazos de entrega",
        }

        return {"sugestoes": sugestoes}
