#!/usr/bin/env python3
"""
Técnicas Básicas de Prompt Engineering
======================================

DEMONSTRAÇÃO COM INPUT ÚNICO:
Todas as técnicas usam o mesmo cenário para mostrar
como diferentes prompts afetam o resultado.

INPUT ÚNICO: Análise de um produto e-commerce
"""

from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage


# ============================================================================
# Configuração e Input Único
# ============================================================================

print("🎯 Prompt Engineering: Técnicas Básicas")
print("📦 CENÁRIO ÚNICO: Análise de Produto E-commerce")
print("=" * 60)

# LLM Configuration
llm = ChatOllama(model="mistral:latest", temperature=0.7)

# 📦 INPUT ÚNICO - Dados do produto
PRODUCT_DATA = """
PRODUTO: Fone de Ouvido Bluetooth Premium XYZ
PREÇO: R$ 299,00
AVALIAÇÕES: 4.2/5 estrelas (847 avaliações)
CARACTERÍSTICAS:
- Cancelamento de ruído ativo
- Bateria 30 horas
- Conectividade Bluetooth 5.0
- Resistente à água IPX4
- Microfone integrado

COMENTÁRIOS DOS CLIENTES:
- "Som excelente, mas o preço é um pouco alto"
- "Bateria dura muito, recomendo!"
- "Cancelamento de ruído funciona bem"
- "Chegou com defeito, tive que trocar"
- "Confortável para usar por horas"
"""

print("📦 DADOS DO PRODUTO:")
print(PRODUCT_DATA)
print("=" * 60)


# ============================================================================
# Técnica 1: Zero-Shot Prompting
# ============================================================================


def zero_shot_analysis():
    """Zero-Shot: Pergunta direta sem contexto adicional"""
    print("\n🎯 TÉCNICA 1: ZERO-SHOT PROMPTING")
    print("-" * 40)
    print("📝 Característica: Pergunta direta, sem exemplos ou contexto")

    prompt = f"""
    Analise este produto:
    
    {PRODUCT_DATA}
    
    Faça uma análise do produto.
    """

    print("💬 Prompt usado: Análise direta e simples")

    response = llm.invoke([HumanMessage(content=prompt)])
    print("\n🤖 RESULTADO ZERO-SHOT:")
    print(f"{response.content.strip()}")

    print("\n✅ Características: Resposta genérica, pode variar muito")
    print("⚠️  Limitações: Falta de direcionamento específico")


# ============================================================================
# Técnica 2: Few-Shot Prompting
# ============================================================================


def few_shot_analysis():
    """Few-Shot: Dar exemplos de como queremos a análise"""
    print("\n🎯 TÉCNICA 2: FEW-SHOT PROMPTING")
    print("-" * 40)
    print("📝 Característica: Fornece exemplos do formato desejado")

    prompt = f"""
    Analise produtos seguindo estes exemplos:
    
    EXEMPLO 1:
    Produto: Smartphone ABC
    Análise: ⭐ PONTOS FORTES: Câmera excelente, bateria duradoura
    ❌ PONTOS FRACOS: Preço elevado, armazenamento limitado
    🎯 RECOMENDAÇÃO: Bom para fotografia, mas caro para uso básico
    
    EXEMPLO 2:
    Produto: Notebook DEF
    Análise: ⭐ PONTOS FORTES: Performance rápida, design elegante
    ❌ PONTOS FRACOS: Tela pequena, aquece muito
    🎯 RECOMENDAÇÃO: Ideal para trabalho, não para jogos
    
    Agora analise este produto seguindo o mesmo formato:
    {PRODUCT_DATA}
    
    Análise:
    """

    print("💬 Prompt usado: Exemplos + formato estruturado")

    response = llm.invoke([HumanMessage(content=prompt)])
    print("\n🤖 RESULTADO FEW-SHOT:")
    print(f"{response.content.strip()}")

    print("\n✅ Características: Formato consistente, estruturado")
    print("⚠️  Limitações: Prompt mais longo")


# ============================================================================
# Técnica 3: Chain of Thought (CoT)
# ============================================================================


def chain_of_thought_analysis():
    """CoT: Pedir raciocínio passo a passo"""
    print("\n🎯 TÉCNICA 3: CHAIN OF THOUGHT")
    print("-" * 40)
    print("📝 Característica: Mostra o processo de raciocínio")

    prompt = f"""
    Analise este produto passo a passo, mostrando seu raciocínio:
    
    {PRODUCT_DATA}
    
    Siga estes passos de análise:
    
    PASSO 1: Analise o preço vs características
    PASSO 2: Avalie as avaliações dos clientes
    PASSO 3: Identifique pontos fortes e fracos
    PASSO 4: Considere o público-alvo
    PASSO 5: Dê sua recomendação final
    
    Mostre seu raciocínio em cada passo:
    """

    print("💬 Prompt usado: Raciocínio estruturado em etapas")

    response = llm.invoke([HumanMessage(content=prompt)])
    print("\n🤖 RESULTADO CHAIN OF THOUGHT:")
    print(f"{response.content.strip()}")

    print("\n✅ Características: Raciocínio transparente, mais confiável")
    print("⚠️  Limitações: Resposta mais longa")


# ============================================================================
# Técnica 4: Role Prompting
# ============================================================================


def role_prompting_analysis():
    """Role Prompting: Assumir papel de especialista"""
    print("\n🎯 TÉCNICA 4: ROLE PROMPTING")
    print("-" * 40)
    print("📝 Característica: Assume papel de especialista")

    prompt = f"""
    Você é um especialista em tecnologia de áudio com 15 anos de experiência 
    analisando fones de ouvido para uma revista técnica renomada.
    
    Seus leitores confiam em suas análises detalhadas e honestas.
    Você conhece profundamente:
    - Qualidade de áudio e drivers
    - Tecnologias de cancelamento de ruído
    - Durabilidade e materiais
    - Custo-benefício do mercado atual
    
    Analise este produto com sua expertise:
    {PRODUCT_DATA}
    
    Escreva uma análise técnica profissional para seus leitores:
    """

    print("💬 Prompt usado: Papel de especialista em áudio")

    response = llm.invoke([HumanMessage(content=prompt)])
    print("\n🤖 RESULTADO ROLE PROMPTING:")
    print(f"{response.content.strip()}")

    print("\n✅ Características: Análise especializada, vocabulário técnico")
    print("⚠️  Limitações: Pode ser muito específico")


# ============================================================================
# Comparação Side-by-Side
# ============================================================================


def side_by_side_comparison():
    """Compara todas as técnicas lado a lado"""
    print("\n📊 COMPARAÇÃO LADO A LADO")
    print("=" * 80)
    print("🎯 MESMO INPUT, DIFERENTES TÉCNICAS:")

    techniques = {
        "Zero-Shot": "Análise direta e genérica",
        "Few-Shot": "Formato estruturado com exemplos",
        "Chain of Thought": "Raciocínio passo a passo",
        "Role Prompting": "Expertise de especialista",
    }

    for technique, description in techniques.items():
        print(f"\n📌 {technique.upper()}:")
        print(f"   Abordagem: {description}")
        print("   Resultado: Varia em especificidade e estrutura")

    print("\n💡 INSIGHTS:")
    print("- Zero-Shot: Mais rápido, menos específico")
    print("- Few-Shot: Formato consistente")
    print("- Chain of Thought: Mais confiável para decisões")
    print("- Role Prompting: Maior profundidade técnica")


# ============================================================================
# Dicas Práticas
# ============================================================================


def practical_tips():
    """Dicas práticas para escolher a técnica"""
    print("\n💡 QUANDO USAR CADA TÉCNICA:")
    print("=" * 50)

    tips = {
        "🎯 Zero-Shot": [
            "✅ Tarefas simples e diretas",
            "✅ Quando velocidade é prioridade",
            "✅ Testes rápidos de conceito",
        ],
        "📚 Few-Shot": [
            "✅ Quando precisa de formato específico",
            "✅ Tarefas de classificação",
            "✅ Quando tem exemplos de qualidade",
        ],
        "🧠 Chain of Thought": [
            "✅ Problemas complexos de raciocínio",
            "✅ Quando precisa entender o 'porquê'",
            "✅ Decisões importantes que precisam justificativa",
        ],
        "👨‍🎓 Role Prompting": [
            "✅ Quando precisa de expertise específica",
            "✅ Análises técnicas profundas",
            "✅ Quando o público-alvo é especializado",
        ],
    }

    for technique, use_cases in tips.items():
        print(f"\n{technique}:")
        for case in use_cases:
            print(f"  {case}")


# ============================================================================
# Execução Principal
# ============================================================================


def main():
    """Executa todas as demonstrações com o mesmo input"""
    try:
        # Demonstrar cada técnica com o mesmo input
        zero_shot_analysis()
        few_shot_analysis()
        chain_of_thought_analysis()
        role_prompting_analysis()

        # Comparação e dicas
        side_by_side_comparison()
        practical_tips()

        print("\n" + "=" * 60)
        print("🎓 CONCLUSÃO:")
        print("O MESMO INPUT pode gerar resultados muito diferentes")
        print("dependendo da técnica de prompt engineering usada!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("Certifique-se que o Ollama está rodando:")
        print("ollama run mistral:latest")


if __name__ == "__main__":
    main()
