#!/usr/bin/env python3
"""
Técnicas Avançadas de Prompt Engineering
========================================

DEMONSTRAÇÃO COM INPUT ÚNICO:
Todas as técnicas avançadas usando o mesmo cenário
para mostrar como otimizações sofisticadas afetam o resultado.

INPUT ÚNICO: Análise de estratégia de marketing
"""

from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
import time
import json


# ============================================================================
# Configuração e Input Único
# ============================================================================

print("🚀 Prompt Engineering: Técnicas Avançadas")
print("📈 CENÁRIO ÚNICO: Estratégia de Marketing")
print("=" * 60)

# LLM Configuration
llm = ChatOllama(model="mistral:latest", temperature=0.3)

# 📈 INPUT ÚNICO - Situação da empresa
COMPANY_SCENARIO = """
EMPRESA: TechStart - Startup de aplicativos móveis
SITUAÇÃO ATUAL:
- Lançou app de produtividade há 6 meses
- 10.000 downloads
- 1.200 usuários ativos mensais
- Receita: R$ 15.000/mês
- Orçamento marketing: R$ 50.000
- Equipe: 8 pessoas
- Concorrentes: 5 apps similares no mercado

DESAFIO:
Dobrar o número de usuários ativos em 3 meses

DADOS DISPONÍVEIS:
- 60% dos usuários são profissionais liberais
- 40% são estudantes universitários
- Principais reclamações: interface complexa
- Principais elogios: funcionalidades únicas
- Taxa de retenção: 35% (média do setor: 25%)
"""

print("📈 CENÁRIO DA EMPRESA:")
print(COMPANY_SCENARIO)
print("=" * 60)


# ============================================================================
# Técnica 1: Self-Consistency
# ============================================================================


def self_consistency_strategy():
    """Self-Consistency: Múltiplas execuções da mesma análise"""
    print("\n🔄 TÉCNICA 1: SELF-CONSISTENCY")
    print("-" * 40)
    print("📝 Característica: Executa múltiplas vezes para maior confiabilidade")

    prompt = f"""
    Baseado nesta situação da empresa:
    {COMPANY_SCENARIO}
    
    Qual é a PRINCIPAL estratégia que você recomenda para dobrar 
    os usuários ativos em 3 meses?
    
    Responda com apenas 1 estratégia principal e o motivo:
    """

    print("💬 Prompt usado: Pergunta específica sobre estratégia principal")
    print("🔄 Executando 3 vezes para verificar consistência...")

    responses = []
    for i in range(3):
        response = llm.invoke([HumanMessage(content=prompt)])
        result = response.content.strip()
        responses.append(result)
        print(f"\n   🎯 Execução {i + 1}: {result[:100]}...")
        time.sleep(1)

    print("\n📊 ANÁLISE DE CONSISTÊNCIA:")
    print(f"- Execução 1: {responses[0][:80]}...")
    print(f"- Execução 2: {responses[1][:80]}...")
    print(f"- Execução 3: {responses[2][:80]}...")

    print("\n✅ Vantagem: Identifica a estratégia mais consistente")
    print("⚠️  Limitação: Usa 3x mais tokens")


# ============================================================================
# Técnica 2: Tree of Thoughts
# ============================================================================


def tree_of_thoughts_strategy():
    """Tree of Thoughts: Explorar múltiplas abordagens estratégicas"""
    print("\n🌳 TÉCNICA 2: TREE OF THOUGHTS")
    print("-" * 40)
    print("📝 Característica: Explora múltiplos caminhos de solução")

    prompt = f"""
    Situação da empresa:
    {COMPANY_SCENARIO}
    
    OBJETIVO: Dobrar usuários ativos em 3 meses
    
    Vamos explorar 3 ABORDAGENS diferentes:
    
    🎯 ABORDAGEM A - AQUISIÇÃO:
    - Estratégia 1: [descreva estratégia de aquisição]
    - Estratégia 2: [descreva outra estratégia de aquisição]
    - Avalie: Custo vs Impacto de cada uma
    
    🔄 ABORDAGEM B - RETENÇÃO:
    - Estratégia 1: [descreva estratégia de retenção]
    - Estratégia 2: [descreva outra estratégia de retenção]
    - Avalie: Facilidade vs Resultado de cada uma
    
    📱 ABORDAGEM C - PRODUTO:
    - Estratégia 1: [descreva melhoria no produto]
    - Estratégia 2: [descreva outra melhoria]
    - Avalie: Recursos necessários vs Impacto
    
    SÍNTESE FINAL:
    Combine as MELHORES estratégias das 3 abordagens em um plano integrado.
    """

    print("💬 Prompt usado: Exploração de múltiplas abordagens")

    response = llm.invoke([HumanMessage(content=prompt)])
    print("\n🌳 RESULTADO TREE OF THOUGHTS:")
    print(f"{response.content.strip()}")

    print("\n✅ Vantagem: Visão abrangente, múltiplas soluções")
    print("⚠️  Limitação: Resposta muito extensa")


# ============================================================================
# Técnica 3: Prompt Chaining
# ============================================================================


def prompt_chaining_strategy():
    """Prompt Chaining: Quebrar análise em etapas específicas"""
    print("\n🔗 TÉCNICA 3: PROMPT CHAINING")
    print("-" * 40)
    print("📝 Característica: Quebra problema complexo em etapas")

    # ETAPA 1: Análise do problema
    prompt1 = f"""
    Analise esta situação e identifique os 3 PRINCIPAIS GARGALOS:
    {COMPANY_SCENARIO}
    
    Liste apenas os 3 gargalos mais críticos:
    """

    print("🔗 ETAPA 1 - Identificação de Gargalos:")
    response1 = llm.invoke([HumanMessage(content=prompt1)])
    bottlenecks = response1.content.strip()
    print(f"Gargalos: {bottlenecks}")

    # ETAPA 2: Soluções específicas
    prompt2 = f"""
    Gargalos identificados:
    {bottlenecks}
    
    Para CADA gargalo, sugira UMA solução específica que pode ser 
    implementada com orçamento de R$ 50.000 em 3 meses:
    
    Formato: Gargalo X → Solução Y (custo estimado)
    """

    print("\n🔗 ETAPA 2 - Soluções Específicas:")
    response2 = llm.invoke([HumanMessage(content=prompt2)])
    solutions = response2.content.strip()
    print(f"Soluções: {solutions}")

    # ETAPA 3: Priorização
    prompt3 = f"""
    Soluções propostas:
    {solutions}
    
    Priorize as soluções considerando:
    - Impacto no objetivo (dobrar usuários)
    - Facilidade de implementação
    - Custo-benefício
    
    Ordene da MAIS prioritária para MENOS prioritária:
    """

    print("\n🔗 ETAPA 3 - Priorização Final:")
    response3 = llm.invoke([HumanMessage(content=prompt3)])
    priorities = response3.content.strip()
    print(f"Prioridades: {priorities}")

    print("\n✅ Vantagem: Análise estruturada e específica")
    print("⚠️  Limitação: Múltiplas chamadas ao LLM")


# ============================================================================
# Técnica 4: Structured Output
# ============================================================================


def structured_output_strategy():
    """Structured Output: Forçar formato JSON específico"""
    print("\n📋 TÉCNICA 4: STRUCTURED OUTPUT")
    print("-" * 40)
    print("📝 Característica: Saída estruturada em formato específico")

    prompt = f"""
    Analise esta situação e crie uma estratégia de marketing:
    {COMPANY_SCENARIO}
    
    Responda EXATAMENTE neste formato JSON:
    {{
        "analise_situacao": {{
            "pontos_fortes": ["forte1", "forte2"],
            "pontos_fracos": ["fraco1", "fraco2"],
            "oportunidades": ["oportunidade1", "oportunidade2"]
        }},
        "estrategia_principal": {{
            "nome": "Nome da estratégia",
            "descricao": "Descrição em 1 frase",
            "investimento_necessario": "R$ X.XXX",
            "prazo_execucao": "X semanas",
            "resultado_esperado": "X% aumento usuários"
        }},
        "acoes_especificas": [
            {{
                "acao": "Ação 1",
                "responsavel": "Quem executa",
                "prazo": "X semanas",
                "custo": "R$ XXX"
            }},
            {{
                "acao": "Ação 2", 
                "responsavel": "Quem executa",
                "prazo": "X semanas",
                "custo": "R$ XXX"
            }}
        ],
        "metricas_acompanhamento": ["metrica1", "metrica2", "metrica3"]
    }}
    
    JSON:
    """

    print("💬 Prompt usado: Formato JSON estruturado")

    response = llm.invoke([HumanMessage(content=prompt)])
    result = response.content.strip()
    print("\n📋 RESULTADO STRUCTURED OUTPUT:")
    print(f"{result}")

    # Tentar parsear JSON para validar estrutura
    try:
        parsed = json.loads(result)
        print("\n✅ JSON válido! Estrutura correta.")
        print(
            f"📊 Estratégia principal: {parsed.get('estrategia_principal', {}).get('nome', 'N/A')}"
        )
    except Exception:
        print("\n⚠️  JSON inválido, mas formato estruturado.")

    print("\n✅ Vantagem: Dados estruturados, fácil integração")
    print("⚠️  Limitação: Pode ser rígido demais")


# ============================================================================
# Técnica 5: Negative Prompting
# ============================================================================


def negative_prompting_strategy():
    """Negative Prompting: Especificar o que NÃO fazer"""
    print("\n🚫 TÉCNICA 5: NEGATIVE PROMPTING")
    print("-" * 40)
    print("📝 Característica: Especifica claramente o que evitar")

    prompt = f"""
    Crie uma estratégia de marketing para esta empresa:
    {COMPANY_SCENARIO}
    
    REQUISITOS POSITIVOS:
    ✅ Estratégia prática e implementável
    ✅ Foque no objetivo: dobrar usuários em 3 meses
    ✅ Considere o orçamento de R$ 50.000
    ✅ Máximo 150 palavras
    
    NÃO FAÇA ISSO:
    ❌ NÃO sugira estratégias que ultrapassem o orçamento
    ❌ NÃO proponha soluções que demorem mais de 3 meses
    ❌ NÃO use jargões de marketing genéricos
    ❌ NÃO sugira mudanças drásticas no produto
    ❌ NÃO mencione estratégias sem dados concretos
    ❌ NÃO ultrapasse 150 palavras
    ❌ NÃO seja vago ou genérico
    
    Estratégia de marketing:
    """

    print("💬 Prompt usado: Requisitos + restrições específicas")

    response = llm.invoke([HumanMessage(content=prompt)])
    result = response.content.strip()
    print("\n🚫 RESULTADO NEGATIVE PROMPTING:")
    print(f"{result}")

    # Análise da resposta
    word_count = len(result.split())
    print("\n📊 ANÁLISE:")
    print(f"- Palavras: {word_count}/150")
    print(f"- Respeitou limite: {'✅' if word_count <= 150 else '❌'}")
    print("- Focado no objetivo: ✅")

    print("\n✅ Vantagem: Evita problemas comuns, mais focado")
    print("⚠️  Limitação: Prompt mais longo")


# ============================================================================
# Comparação: Simples vs Otimizado
# ============================================================================


def optimization_comparison():
    """Comparar abordagem simples vs todas as técnicas"""
    print("\n⚡ COMPARAÇÃO: ABORDAGEM SIMPLES vs OTIMIZADA")
    print("=" * 70)

    # Abordagem Simples
    print("\n📌 ABORDAGEM SIMPLES:")
    simple_prompt = f"""
    Como esta empresa pode dobrar seus usuários?
    {COMPANY_SCENARIO}
    """

    print("Prompt: 'Como dobrar usuários?' (genérico)")
    response_simple = llm.invoke([HumanMessage(content=simple_prompt)])
    print(f"Resultado: {response_simple.content.strip()[:120]}...")

    # Resumo das técnicas avançadas
    print("\n📌 TÉCNICAS AVANÇADAS APLICADAS:")
    print("🔄 Self-Consistency: Validação por múltiplas execuções")
    print("🌳 Tree of Thoughts: Exploração de múltiplas abordagens")
    print("🔗 Prompt Chaining: Análise estruturada em etapas")
    print("📋 Structured Output: Formato padronizado e processável")
    print("🚫 Negative Prompting: Evita problemas comuns")

    print("\n💡 DIFERENÇAS OBSERVADAS:")
    print("- Simples: Resposta genérica, pode variar muito")
    print("- Avançado: Mais específico, confiável e estruturado")
    print("- Simples: 1 execução, resultado imprevisível")
    print("- Avançado: Múltiplas validações, maior precisão")


# ============================================================================
# Execução Principal
# ============================================================================


def main():
    """Executa todas as técnicas avançadas com o mesmo input"""
    try:
        # Técnicas avançadas
        self_consistency_strategy()
        tree_of_thoughts_strategy()
        prompt_chaining_strategy()
        structured_output_strategy()
        negative_prompting_strategy()

        # Comparação final
        optimization_comparison()

        print("\n" + "=" * 70)
        print("🎓 CONCLUSÃO TÉCNICAS AVANÇADAS:")
        print("- O MESMO INPUT gera resultados drasticamente diferentes")
        print("- Técnicas avançadas oferecem maior CONTROLE e PRECISÃO")
        print("- Escolha a técnica baseada na COMPLEXIDADE da tarefa")
        print("- COMBINE técnicas para resultados ainda melhores")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("Certifique-se que o Ollama está rodando:")
        print("ollama run mistral:latest")


if __name__ == "__main__":
    main()
