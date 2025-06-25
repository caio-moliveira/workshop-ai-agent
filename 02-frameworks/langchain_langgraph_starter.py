#!/usr/bin/env python3
"""
Fluxo Simples de Agentes de IA
==============================

Três agentes especializados trabalham em sequência:
- 🏷️  Agent Classifier: Especialista em categorizar textos
- 🔍 Agent Keywords: Especialista em identificar palavras-chave
- 📝 Agent Summarizer: Especialista em resumir textos

Cada agente tem sua própria "personalidade" e foco específico.
"""

import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage


# ============================================================================
# Visualização do Gráfico
# ============================================================================


def save_graph_visualization(team, filename="agents_workflow.png"):
    """Salva a visualização do gráfico da equipe de agentes"""
    try:
        print("\n📊 Gerando visualização do workflow...")

        # Gerar o gráfico em PNG
        graph_png = team.get_graph().draw_mermaid_png()

        # Salvar o arquivo
        with open(filename, "wb") as f:
            f.write(graph_png)

        print(f"✅ Gráfico salvo como: {filename}")
        print("📁 Abra o arquivo para ver o fluxo dos agentes!")

        return filename

    except Exception as e:
        print(f"⚠️  Erro ao gerar visualização: {e}")
        print("💡 Dica: Instale as dependências: pip install pygraphviz")
        return None


# ============================================================================
# Configuração
# ============================================================================

print("🤖 Inicializando equipe de agentes com Ollama + Mistral")
llm = ChatOllama(model="mistral:latest", temperature=0)


# ============================================================================
# Estado Compartilhado - Memória da equipe
# ============================================================================


class TeamState(TypedDict):
    """Memória compartilhada entre os agentes"""

    original_text: str  # Texto original para análise
    category: str  # Categoria identificada pelo Classifier
    important_terms: List[str]  # Palavras-chave encontradas pelo Keywords
    summary: str  # Resumo criado pelo Summarizer
    current_agent: str  # Qual agente está trabalhando agora


# ============================================================================
# Agente 1: Classifier - Especialista em Categorização
# ============================================================================


def agent_classifier(state: TeamState):
    """
    🏷️ Agent Classifier
    Especialista em identificar o tipo/categoria de textos
    """
    print("\n🏷️  Agent Classifier está analisando...")
    print("   Especialidade: Categorização de textos")

    # Prompt especializado para classificação
    prompt = f"""
    Você é um especialista em classificação de textos.
    Sua única tarefa é identificar a categoria do texto.
    
    Classifique este texto em UMA dessas categorias:
    - Notícia
    - Blog Pessoal  
    - Artigo Técnico
    - Marketing
    - Educacional
    - Outros
    
    Texto para analisar:
    {state["original_text"]}
    
    Responda apenas com a categoria:
    """

    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    category = response.content.strip()

    print(f"   📂 Categoria identificada: {category}")

    return {"category": category, "current_agent": "Classifier"}


# ============================================================================
# Agente 2: Keywords - Especialista em Palavras-chave
# ============================================================================


def agent_keywords(state: TeamState):
    """
    🔍 Agent Keywords
    Especialista em extrair palavras-chave importantes
    """
    print("\n🔍 Agent Keywords está analisando...")
    print("   Especialidade: Identificação de palavras-chave")

    # Prompt especializado para keywords
    prompt = f"""
    Você é um especialista em análise de palavras-chave.
    Sua tarefa é encontrar as 5 palavras-chave mais importantes do texto.
    
    Categoria já identificada: {state["category"]}
    
    Texto para analisar:
    {state["original_text"]}
    
    Extraia exatamente 5 palavras-chave importantes, separadas por vírgula.
    Foque em: conceitos principais, nomes importantes, tecnologias, lugares.
    
    Palavras-chave:
    """

    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    keywords_text = response.content.strip()
    keywords = [kw.strip() for kw in keywords_text.split(",")]

    print(f"   🔑 Palavras-chave: {keywords}")

    return {"important_terms": keywords, "current_agent": "Keywords"}


# ============================================================================
# Agente 3: Summarizer - Especialista em Resumos
# ============================================================================


def agent_summarizer(state: TeamState):
    """
    📝 Agent Summarizer
    Especialista em criar resumos concisos e informativos
    """
    print("\n📝 Agent Summarizer está analisando...")
    print("   Especialidade: Criação de resumos")

    # Prompt especializado para resumo
    prompt = f"""
    Você é um especialista em criar resumos concisos.
    Sua tarefa é resumir o texto em máximo 15 palavras.
    
    Informações dos outros agentes:
    - Categoria: {state["category"]}
    - Palavras-chave: {", ".join(state["important_terms"])}
    
    Texto para resumir:
    {state["original_text"]}
    
    Crie um resumo de máximo 15 palavras que capture a essência:
    """

    message = HumanMessage(content=prompt)
    response = llm.invoke([message])
    summary = response.content.strip()

    print(f"   📋 Resumo: {summary}")

    return {"summary": summary, "current_agent": "Summarizer"}


# ============================================================================
# Criando a Equipe de Agentes
# ============================================================================


def create_agents_team():
    """Cria a equipe de agentes especializados"""
    print("\n🔧 Montando equipe de agentes...")

    # Criar o workflow
    workflow = StateGraph(TeamState)

    # Adicionar cada agente especializado
    workflow.add_node("classifier", agent_classifier)
    workflow.add_node("keyword_agent", agent_keywords)
    workflow.add_node("summarizer", agent_summarizer)

    # Definir o fluxo de trabalho da equipe
    workflow.set_entry_point("classifier")  # Começa com classificação
    workflow.add_edge("classifier", "keyword_agent")  # Depois identifica keywords
    workflow.add_edge("keyword_agent", "summarizer")  # Por fim, cria resumo
    workflow.add_edge("summarizer", END)  # Trabalho concluído

    # Compilar a equipe
    team = workflow.compile()
    print("✅ Equipe de agentes pronta para trabalhar!")

    return team


# ============================================================================
# Testando Nossa Equipe
# ============================================================================


def test_agents_team():
    """Testa nossa equipe de agentes com texto de exemplo"""
    print("\n" + "=" * 70)
    print("🚀 EQUIPE DE AGENTES EM AÇÃO")
    print("=" * 70)

    # Criar a equipe
    team = create_agents_team()

    # Tentar salvar visualização
    save_graph_visualization(team)

    # Texto de exemplo
    sample_text = """
    A OpenAI lançou o ChatGPT-4, uma nova versão do seu modelo de linguagem 
    que promete revolucionar a forma como interagimos com inteligência artificial. 
    O modelo apresenta melhorias significativas em raciocínio, criatividade e 
    capacidades multimodais, sendo capaz de processar tanto texto quanto imagens. 
    A empresa espera que esta tecnologia impacte positivamente diversos setores, 
    desde educação até desenvolvimento de software.
    """

    print("\n📖 Texto para análise:")
    print(f"   {sample_text.strip()}")
    print("\n" + "-" * 70)
    print("🔄 Iniciando análise colaborativa...")

    # Executar a análise em equipe
    result = team.invoke({"original_text": sample_text, "current_agent": "Iniciando"})

    # Mostrar resultados finais
    print("\n" + "=" * 70)
    print("📊 RELATÓRIO FINAL DA EQUIPE")
    print("=" * 70)
    print(f"🏷️  Categoria: {result['category']}")
    print(f"🔑 Palavras-chave: {', '.join(result['important_terms'])}")
    print(f"📋 Resumo: {result['summary']}")
    print(f"👥 Último agente: {result['current_agent']}")
    print("\n✨ Análise colaborativa concluída!")

    return result


def test_different_texts():
    """Testa com diferentes tipos de texto"""
    team = create_agents_team()

    texts = {
        "Blog Pessoal": "Hoje acordei cedo e fui correr no parque. O dia estava lindo e consegui fazer 5km. Me sinto muito bem depois do exercício e pronto para mais um dia produtivo de trabalho.",
        "Notícia": "O governo brasileiro anunciou hoje novas medidas econômicas para combater a inflação. O Banco Central deve aumentar a taxa Selic na próxima reunião do Copom.",
        "Artigo Técnico": "Machine Learning é um subcampo da inteligência artificial que permite que sistemas aprendam automaticamente sem serem explicitamente programados. Algoritmos como Random Forest e Neural Networks são amplamente utilizados.",
    }

    print("\n" + "=" * 70)
    print("🔬 TESTANDO DIFERENTES TIPOS DE TEXTO")
    print("=" * 70)

    for text_type, text in texts.items():
        print(f"\n📄 Testando: {text_type}")
        print(f"Texto: {text[:60]}...")
        print("-" * 50)

        result = team.invoke({"original_text": text})

        print(f"🏷️  {result['category']}")
        print(
            f"🔑 {', '.join(result['important_terms'][:3])}..."
        )  # Primeiras 3 keywords
        print(f"📋 {result['summary']}")


# ============================================================================
# Execução Principal
# ============================================================================


def main():
    """Função principal - executa os testes da equipe"""
    print("🌟 SISTEMA DE AGENTES ESPECIALIZADOS")
    print("Cada agente tem sua especialidade e trabalha em equipe!")
    print("=" * 70)

    try:
        # Teste principal
        test_agents_team()

        # Testes com textos variados
        # test_different_texts()

        print("\n" + "=" * 70)
        print("💡 DICAS:")
        print("- Verifique o arquivo 'agents_workflow.png' para ver o gráfico!")
        print("- Use um visualizador de imagem para abrir o arquivo PNG")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("Certifique-se que o Ollama está rodando:")
        print("ollama run mistral:latest")


if __name__ == "__main__":
    main()
