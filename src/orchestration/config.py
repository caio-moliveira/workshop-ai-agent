"""
Configuração Simples do LangSmith para Demonstração Multi-Agente
Foco em mostrar como os agentes se comunicam e são observados
"""

import os
from typing import Dict, Any
from langsmith import traceable

# Imports LangSmith
try:
    from langsmith import traceable

    LANGSMITH_AVAILABLE = True
    print("✅ LangSmith disponível")
except ImportError:
    print("⚠️  LangSmith não instalado. Instale com: pip install langsmith")
    LANGSMITH_AVAILABLE = False

    # Mock decorator para desenvolvimento sem LangSmith
    def traceable(name=None, **kwargs):
        def decorator(func):
            return func

        return decorator


class SimpleLangSmithConfig:
    """
    Configuração simples do LangSmith para demonstrações educacionais
    """

    def __init__(self, project_name: str = "demo-multi-agentes"):
        self.project_name = project_name
        self.setup_environment()

    def setup_environment(self):
        """Configura LangSmith de forma simples"""
        if LANGSMITH_AVAILABLE:
            # Configurar variáveis de ambiente
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = self.project_name

            # Verificar se API key está configurada
            if not os.getenv("LANGSMITH_API_KEY"):
                print("""
🔑 Para ativar o tracing no LangSmith:
1. Crie uma conta em https://smith.langchain.com
2. Configure a API key:
   export LANGSMITH_API_KEY="sua-api-key-aqui"
3. Execute novamente o código
                """)
            else:
                print(f"🔍 Tracing ativo no projeto: {self.project_name}")
        else:
            print("📝 Executando sem tracing (apenas logs locais)")

    def trace_coordenador(self, func):
        """Decorator para tracear o Agente Coordenador"""
        if not LANGSMITH_AVAILABLE:
            return func

        return traceable(
            name="Agente_Coordenador",
            project_name=self.project_name,
            tags=["coordenador", "analise"],
        )(func)

    def trace_agente_tecnico(self, func):
        """Decorator para tracear o Agente Técnico"""
        if not LANGSMITH_AVAILABLE:
            return func

        return traceable(
            name="Agente_Tecnico",
            project_name=self.project_name,
            tags=["tecnico", "resolucao"],
        )(func)

    def trace_agente_financeiro(self, func):
        """Decorator para tracear o Agente Financeiro"""
        if not LANGSMITH_AVAILABLE:
            return func

        return traceable(
            name="Agente_Financeiro",
            project_name=self.project_name,
            tags=["financeiro", "cobranca"],
        )(func)

    def trace_agente_geral(self, func):
        """Decorator para tracear o Agente Geral"""
        if not LANGSMITH_AVAILABLE:
            return func

        return traceable(
            name="Agente_Geral",
            project_name=self.project_name,
            tags=["geral", "informacoes"],
        )(func)

    def trace_workflow(self, func):
        """Decorator para tracear o Workflow completo"""
        if not LANGSMITH_AVAILABLE:
            return func

        return traceable(
            name="Workflow_MultiAgente",
            project_name=self.project_name,
            tags=["workflow", "orquestracao"],
        )(func)

    def log_simple(self, message: str, agent_name: str = "Sistema"):
        """Log simples para acompanhar execução"""
        print(f"[{agent_name}] {message}")


# === CONFIGURAÇÃO GLOBAL ===

# Criar instância global para facilitar uso
langsmith_config = SimpleLangSmithConfig()


# === DECORATORS PRONTOS PARA USO ===


def trace_coordenador(func):
    """Decorator pronto para o Agente Coordenador"""
    decorated = langsmith_config.trace_coordenador(func)

    def wrapper(*args, **kwargs):
        langsmith_config.log_simple("🎯 Analisando consulta...", "Coordenador")
        result = decorated(*args, **kwargs)
        langsmith_config.log_simple(
            f"✅ Análise completa - Categoria: {result.get('category', 'N/A')}",
            "Coordenador",
        )
        return result

    return wrapper


def trace_agente_tecnico(func):
    """Decorator pronto para o Agente Técnico"""
    decorated = langsmith_config.trace_agente_tecnico(func)

    def wrapper(*args, **kwargs):
        langsmith_config.log_simple("🔧 Processando problema técnico...", "Técnico")
        result = decorated(*args, **kwargs)
        langsmith_config.log_simple("✅ Solução técnica fornecida", "Técnico")
        return result

    return wrapper


def trace_agente_financeiro(func):
    """Decorator pronto para o Agente Financeiro"""
    decorated = langsmith_config.trace_agente_financeiro(func)

    def wrapper(*args, **kwargs):
        langsmith_config.log_simple(
            "💰 Processando questão financeira...", "Financeiro"
        )
        result = decorated(*args, **kwargs)
        langsmith_config.log_simple("✅ Resposta financeira pronta", "Financeiro")
        return result

    return wrapper


def trace_agente_geral(func):
    """Decorator pronto para o Agente Geral"""
    decorated = langsmith_config.trace_agente_geral(func)

    def wrapper(*args, **kwargs):
        langsmith_config.log_simple("ℹ️  Fornecendo informações gerais...", "Geral")
        result = decorated(*args, **kwargs)
        langsmith_config.log_simple("✅ Informações fornecidas", "Geral")
        return result

    return wrapper


def trace_workflow(func):
    """Decorator pronto para o Workflow"""
    decorated = langsmith_config.trace_workflow(func)

    def wrapper(*args, **kwargs):
        query = args[0] if args else kwargs.get("query", "N/A")
        langsmith_config.log_simple(
            f"🚀 Iniciando processamento: '{query[:50]}...'", "Workflow"
        )
        result = decorated(*args, **kwargs)
        agent_usado = result.get("agent_used", "N/A")
        langsmith_config.log_simple(
            f"🎉 Processamento concluído por: {agent_usado}", "Workflow"
        )
        return result

    return wrapper


# === FUNÇÃO DE SETUP RÁPIDO ===


def setup_simple_tracing(project_name: str = "demo-multi-agentes"):
    """
    Setup rápido para demonstrações
    """
    global langsmith_config
    langsmith_config = SimpleLangSmithConfig(project_name)

    print(f"""
🎓 DEMO MULTI-AGENTES CONFIGURADO
📁 Projeto: {project_name}
🔍 Para ver os traces:
   1. Acesse https://smith.langchain.com
   2. Vá para o projeto '{project_name}'
   3. Execute o código e veja os agentes em ação!
    """)

    return langsmith_config


# === EXEMPLO DE USO SIMPLES ===

if __name__ == "__main__":
    # Setup
    config = setup_simple_tracing("exemplo-educacional")

    # Exemplo de função com tracing
    @trace_agente_tecnico
    def exemplo_agente_tecnico(state: Dict[str, Any]) -> Dict[str, Any]:
        """Exemplo simples de agente técnico"""
        query = state.get("query", "")

        # Simular processamento
        import time

        time.sleep(0.5)

        return {"response": f"Solução técnica para: {query}", "agent_used": "Técnico"}

    # Teste
    resultado = exemplo_agente_tecnico({"query": "Como resolver problema de login?"})
    print(f"Resultado: {resultado['response']}")
    print("\n✅ Verifique o LangSmith para ver o trace!")
