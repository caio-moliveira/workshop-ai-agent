"""
Exemplo Completo - Sistema Multi-Agente com LangSmith
Execute este arquivo para ver os agentes funcionando no LangSmith
"""

import os
from dotenv import load_dotenv
from graph.workflow_suporte import criar_workflow

# Carregar variáveis de ambiente
load_dotenv()

# Configurar LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv(
    "LANGSMITH_PROJECT", "pr-dependable-suppression-55"
)
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv(
    "LANGSMITH_ENDPOINT", "https://api.smith.langchain.com"
)
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")

print(f"🔍 LangSmith configurado para projeto: {os.environ['LANGCHAIN_PROJECT']}")
print(f"🌐 Endpoint: {os.environ['LANGCHAIN_ENDPOINT']}")

# Imports do sistema


def main():
    """Função principal para demonstração"""

    print("\n" + "=" * 60)
    print("🎓 DEMO SISTEMA MULTI-AGENTE")
    print("🔍 Acompanhe no LangSmith!")
    print("=" * 60)

    # Criar workflow
    workflow = criar_workflow()

    # Casos de teste para demonstração
    casos_teste = [
        {
            "query": "Não consigo fazer login no sistema",
            "esperado": {"categoria": "Technical", "agente": "Técnico"},
        },
        {
            "query": "Fui cobrado em duplicata no meu cartão",
            "esperado": {"categoria": "Billing", "agente": "Financeiro"},
        },
        {
            "query": "Qual o horário de funcionamento da empresa?",
            "esperado": {"categoria": "General", "agente": "Geral"},
        },
        {
            "query": "O sistema travou e perdi todos os meus dados! Estou muito irritado!",
            "esperado": {
                "categoria": "Technical",
                "agente": "Escalação",
                "escalado": True,
            },
        },
    ]

    # Processar cada caso
    for i, caso in enumerate(casos_teste, 1):
        print(f"\n📝 CASO {i}: {caso['query']}")
        print("-" * 50)

        # Processar consulta
        resultado = workflow.processar_consulta(caso["query"])

        # Exibir resultados
        print(f"📂 Categoria: {resultado['category']}")
        print(f"😊 Sentimento: {resultado['sentiment']}")
        print(f"🤖 Agente Usado: {resultado['agent_used']}")
        print(f"🚨 Escalado: {'Sim' if resultado['escalated'] else 'Não'}")
        print(f"⏰ Processado em: {resultado['timestamp']}")
        print(f"💬 Resposta: {resultado['response'][:100]}...")

        # Verificar se bateu com o esperado
        esperado = caso["esperado"]
        if resultado["category"] == esperado.get("categoria"):
            print("✅ Categoria correta!")
        if resultado["escalated"] == esperado.get("escalado", False):
            print("✅ Escalação correta!")

        print()

    print("=" * 60)
    print("🎉 DEMONSTRAÇÃO COMPLETA!")
    print("🔍 Veja os traces em: https://smith.langchain.com")
    print(f"📁 Projeto: {os.environ['LANGCHAIN_PROJECT']}")
    print("=" * 60)


if __name__ == "__main__":
    print("🚀 INICIANDO DEMO SISTEMA MULTI-AGENTE")
    # Executar demonstração principal
    main()

    print("\n🎓 FIM DA DEMONSTRAÇÃO")
