#!/usr/bin/env python3
"""
Exemplo AutoGen: Colaboração de Agentes de IA
Este exemplo demonstra como criar agentes de IA que trabalham juntos
para resolver um problema usando o framework AutoGen.
"""

import autogen
from autogen import AssistantAgent, UserProxyAgent

# Configuração para usar Ollama localmente (sem necessidade de chave API!)
config_list = [
    {
        "model": "mistral:latest",  # ou outro modelo Ollama que você tenha instalado
        "base_url": "http://localhost:11434/v1",  # URL padrão do Ollama
        "api_key": "ollama",  # Ollama não precisa de chave real, mas é obrigatório informar algo
        "api_type": "openai",  # Usa a API compatível com OpenAI do Ollama
        "price": [0, 0],  # Preço fictício, pois Ollama é gratuito
    }
]

# Configuração do LLM
llm_config = {
    "config_list": config_list,
    "temperature": 0.7,
    "timeout": 120,
}


def advanced_example():
    """
    Exemplo com múltiplos agentes e chat em grupo
    """
    print("🚀 Exemplo AutoGen: Resolução de Problemas Multi-Agente")
    print("=" * 60)

    # Criar múltiplos agentes especializados
    pesquisador = AssistantAgent(
        name="Pesquisador",
        system_message="""Você é um especialista em pesquisa. Você coleta informações e fatos sobre tópicos.
        Sempre forneça informações precisas e relevantes sobre o assunto solicitado.""",
        llm_config=llm_config,
    )

    escritor = AssistantAgent(
        name="Escritor",
        system_message="""Você é um escritor criativo. Você pega pesquisas e as transforma em conteúdo envolvente.
        Escreva de forma clara, interessante e adequada para o público-alvo.""",
        llm_config=llm_config,
    )

    critico = AssistantAgent(
        name="Critico",
        system_message="""Você é um crítico que revisa conteúdo e sugere melhorias.
        Analise o conteúdo de forma construtiva e forneça sugestões específicas para melhorar.""",
        llm_config=llm_config,
    )

    usuario_proxy = UserProxyAgent(
        name="Usuario",
        human_input_mode="NEVER",  # Mude para "ALWAYS" se quiser entrada manual
        max_consecutive_auto_reply=2,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINAR"),
        code_execution_config=False,  # Desabilita execução de código para este exemplo
    )

    # Criar um chat em grupo com múltiplos agentes
    chat_grupo = autogen.GroupChat(
        agents=[usuario_proxy, pesquisador, escritor, critico],
        messages=[],
        max_round=8,  # Máximo de 8 rodadas de conversa
    )

    # Criar um gerenciador de chat em grupo
    gerenciador = autogen.GroupChatManager(
        groupchat=chat_grupo,
        llm_config=llm_config,
    )

    # Iniciar a discussão em grupo
    tarefa = """
    Criem uma explicação curta e envolvente sobre energias renováveis para estudantes do ensino médio.
    
    Pesquisador: Colete fatos importantes sobre energias renováveis
    Escritor: Crie uma explicação envolvente baseada na pesquisa
    Crítico: Revise e sugira melhorias
    
    Terminem com 'TERMINAR' quando estiverem satisfeitos com a explicação final.
    """

    print("Iniciando a conversa entre os agentes...")
    print("-" * 40)

    # Iniciar o chat
    usuario_proxy.initiate_chat(
        recipient=gerenciador,
        message=tarefa,
    )


if __name__ == "__main__":
    print("🤖 Demonstração do Framework AutoGen")
    print("Este exemplo mostra como agentes de IA podem colaborar!")
    print("\nRecursos demonstrados:")
    print("✓ Criação de agentes de IA especializados")
    print("✓ Comunicação entre agentes")
    print("✓ Mensagens de sistema baseadas em papéis")
    print("✓ Controle de fluxo de conversa")
    print("✓ Chat em grupo com múltiplos agentes")
    print("✓ Colaboração para resolver problemas complexos")
    print("\n" + "=" * 60)

    # Executar o exemplo
    advanced_example()

    print("\n🎉 Demonstração concluída!")
    print("\nPara executar este exemplo:")
    print("1. Instalar Ollama: https://ollama.ai")
    print("2. Baixar um modelo: ollama pull llama3.1:8b")
    print("3. Iniciar Ollama: ollama serve")
    print("4. Instalar AutoGen: pip install pyautogen")
    print("5. Executar o script!")
    print("\n💡 Vantagens do Ollama:")
    print("   • Funciona totalmente offline")
    print("   • Não precisa de chave API")
    print("   • Não tem custos de uso")
    print("   • Dados ficam no seu computador")
    print("\n🔧 Modelos recomendados para começar:")
    print("   • llama3.1:8b (mais rápido)")
    print("   • llama3.1:13b (melhor qualidade)")
    print("   • codellama:7b (especializado em código)")
