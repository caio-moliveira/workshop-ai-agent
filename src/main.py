"""
Exemplo Completo - Sistema Multi-Agente com LangSmith
Execute este arquivo para ver os agentes funcionando no LangSmith
"""

import os
from dotenv import load_dotenv
from graph.workflow_suporte import criar_workflow

# Carregar variáveis de ambiente
load_dotenv()

# Configurar OpenAI API Key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Verificar se API key está configurada
if not os.getenv("OPENAI_API_KEY"):
    print("❌ ERRO: OPENAI_API_KEY não encontrada no arquivo .env")
    exit(1)

# Configurar LangSmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv(
    "LANGSMITH_PROJECT", "demo-sistema-multi-agente"
)
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv(
    "LANGSMITH_ENDPOINT", "https://api.smith.langchain.com"
)
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")


def main():
    """Função principal para demonstração educacional"""

    print("🎓 DEMO SISTEMA MULTI-AGENTE")
    print("=" * 50)

    try:
        workflow = criar_workflow()
    except Exception as e:
        print(f"❌ Erro ao criar workflow: {e}")
        return

    # Casos de teste para demonstração educacional
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
    sucessos = 0
    for i, caso in enumerate(casos_teste, 1):
        print(f"\n📝 CASO {i}: {caso['query']}")

        try:
            resultado = workflow.processar_consulta(caso["query"])

            # Verificar se bateu com o esperado
            esperado = caso["esperado"]
            categoria_correta = resultado["category"] == esperado.get("categoria")
            escalacao_correta = resultado["escalated"] == esperado.get(
                "escalado", False
            )

            if categoria_correta and escalacao_correta:
                print("✅ Resultado correto!")
                sucessos += 1
            else:
                print(
                    f"⚠️ Esperado: {esperado.get('categoria')}, Obtido: {resultado['category']}"
                )

        except Exception as e:
            print(f"❌ Erro no caso {i}: {e}")

    # Resumo final
    print(f"\n🎉 Concluído: {sucessos}/{len(casos_teste)} casos corretos")
    if os.getenv("LANGSMITH_API_KEY"):
        print(
            f"🔍 Traces: https://smith.langchain.com (projeto: {os.environ['LANGCHAIN_PROJECT']})"
        )


if __name__ == "__main__":
    main()
