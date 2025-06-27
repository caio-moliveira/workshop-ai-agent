"""
Sistema de Memória Simples usando LangGraph Checkpointer
Implementação minimalista seguindo padrão oficial
"""

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.memory import InMemoryStore
from langchain_core.messages import HumanMessage
import sqlite3
import os

# === CONFIGURAÇÃO GLOBAL DE MEMÓRIA ===

# Memória de longo prazo - persiste entre conversas
in_memory_store = InMemoryStore()

# Criar diretório se não existir
db_path = "src/memory/conversas.db"
os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)


# Memória de curto prazo - persiste dentro de uma thread/conversa
# Criar conexão SQLite explicitamente
def criar_checkpointer():
    """Cria checkpointer SQLite de forma segura"""
    try:
        # Método mais seguro para criar SqliteSaver
        conn = sqlite3.connect(db_path, check_same_thread=False)
        checkpointer = SqliteSaver(conn)
        return checkpointer
    except Exception as e:
        print(f"⚠️ Erro ao criar SqliteSaver: {e}")
        print("🔄 Usando MemorySaver como fallback")
        from langgraph.checkpoint.memory import MemorySaver

        return MemorySaver()


checkpointer = criar_checkpointer()

# === FUNÇÃO PARA CONFIGURAR MEMÓRIA ===


def configurar_memoria_sistema():
    """
    Configura sistema de memória global para todos os agentes
    """
    print("🧠 Configurando sistema de memória...")
    if isinstance(checkpointer, SqliteSaver):
        print("✅ SqliteSaver (persistente) configurado")
        print(f"📁 Arquivo: {os.path.abspath(db_path)}")
    else:
        print("✅ MemorySaver (temporário) configurado")
    print("✅ InMemoryStore (longo prazo) configurado")

    return checkpointer, in_memory_store


# === FUNÇÃO PARA PROCESSAR COM MEMÓRIA ===


def processar_com_memoria(agente, query: str, thread_id: str = "default"):
    """
    Processa consulta mantendo contexto da conversa

    Args:
        agente: Agente criado com create_react_agent
        query: Consulta do usuário
        thread_id: Identificador da conversa (para manter contexto)
    """

    # Configuração para usar thread específica
    config = {"configurable": {"thread_id": thread_id}}

    # Input para o agente
    input_data = {"messages": [HumanMessage(content=query)]}

    # Processar com memória
    resultado = agente.invoke(input_data, config=config)

    return resultado
