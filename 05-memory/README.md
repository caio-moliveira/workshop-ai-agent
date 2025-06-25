# 05-memory

Esta pasta demonstra implementações avançadas de **sistemas de memória para agentes de IA**, mostrando como agentes podem lembrar e aprender com conversas anteriores usando diferentes abordagens de armazenamento.

## 📁 Arquivos

### `crewai_memory_example.py`
**Sistema de memória avançado com CrewAI + ChromaDB**

**Características:**
- **Memória de Curto Prazo**: ChromaDB para recuperação rápida
- **Memória de Longo Prazo**: SQLite para persistência histórica
- **Memória de Entidades**: Reconhecimento e lembrança de pessoas/objetos
- **Agente Amigável**: Companion AI que constrói relacionamentos

**Tipos de Memória:**
1. **Short-term Memory**: Conversas recentes via RAG storage
2. **Long-term Memory**: Histórico persistente via SQLite
3. **Entity Memory**: Extração e lembrança de entidades importantes

**Funcionalidades:**
- Interface interativa de chat
- Continuidade entre sessões
- Personalização baseada em histórico
- Armazenamento local seguro

### `langchain_memory_example.py`
**Interface Gradio com LangChain + ChromaDB**

**Características:**
- **Interface Web**: Gradio para interação visual
- **Multi-usuário**: Diferentes sessões isoladas
- **Persistência**: ChromaDB para armazenamento vetorial
- **Memory Management**: Gestão automática de contexto

**Funcionalidades:**
- Chat multi-usuário com IDs separados
- Visualização de dados armazenados no ChromaDB
- Limpeza seletiva de dados por usuário
- Carregamento automático de conversas anteriores

### `crewai_memory/` (Pasta gerada)
**Armazenamento persistente do CrewAI**
- `entities/`: Memória de entidades (ChromaDB)
- `short_term/`: Memória de curto prazo (ChromaDB)
- `long_term_memory_storage.db`: Memória de longo prazo (SQLite)
- `latest_kickoff_task_outputs.db`: Cache de resultados

### `data/` (Pasta gerada)
**Armazenamento do LangChain**
- ChromaDB persistente para conversas do Gradio
- Índices vetoriais para busca semântica

## 🚀 Como usar

### 1. CrewAI Memory System

```bash
# Executar agente amigável com memória
python crewai_memory_example.py

# Configurar OpenAI (obrigatório para CrewAI)
export OPENAI_API_KEY="sua-chave-aqui"
```

**Fluxo de uso:**
1. Agente se apresenta e pergunta seu nome
2. Compartilhe informações pessoais (hobbies, trabalho, etc.)
3. Encerre e reinicie - o agente lembrará de você
4. Construa um relacionamento ao longo de múltiplas sessões

### 2. LangChain Gradio Interface

```bash
# Iniciar interface web
python langchain_memory_example.py

# Acessar via browser (URL será exibida)
```

**Funcionalidades da interface:**
- **Seletor de usuário**: Troque entre User 1, 2, 3
- **Chat persistente**: Conversas são salvas automaticamente
- **Visualizar dados**: Botão para ver ChromaDB storage
- **Limpar dados**: Resetar histórico de usuário específico

## 🧠 Arquiteturas de Memória

### CrewAI Memory Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Short-term        │    │   Long-term         │    │   Entity            │
│   Memory            │    │   Memory            │    │   Memory            │
│                     │    │                     │    │                     │
│ ┌─────────────────┐ │    │ ┌─────────────────┐ │    │ ┌─────────────────┐ │
│ │   ChromaDB      │ │    │ │   SQLite        │ │    │ │   ChromaDB      │ │
│ │   RAG Storage   │ │    │ │   Database      │ │    │ │   Entities      │ │
│ └─────────────────┘ │    │ └─────────────────┘ │    │ └─────────────────┘ │
│                     │    │                     │    │                     │
│ Recent context      │    │ Persistent history  │    │ People, places,     │
│ Fast retrieval      │    │ Long conversations  │    │ concepts, events    │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

### LangChain Memory Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Gradio Web Interface                         │
├─────────────────────────────────────────────────────────────────┤
│  User 1    │    User 2    │    User 3    │   ChromaDB Viewer    │
├─────────────────────────────────────────────────────────────────┤
│                         LangChain                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ ChatHistory     │  │ ChromaDB        │  │ Memory Manager  │  │
│  │ Session Store   │  │ Vector Store    │  │ Context Window  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## 💾 Tipos de Memória

### 1. Short-term Memory (Memória de Curto Prazo)
**Propósito**: Contexto imediato e recuperação rápida
- **Storage**: ChromaDB com embeddings
- **Timeframe**: Sessão atual + algumas anteriores
- **Uso**: Manter contexto da conversa atual
- **Vantagens**: Busca semântica rápida

### 2. Long-term Memory (Memória de Longo Prazo)
**Propósito**: Histórico persistente e aprendizado
- **Storage**: SQLite relacional
- **Timeframe**: Indefinido
- **Uso**: Histórico completo, padrões de comportamento
- **Vantagens**: Estrutura relacional, consultas complexas

### 3. Entity Memory (Memória de Entidades)
**Propósito**: Reconhecimento e rastreamento de entidades
- **Storage**: ChromaDB especializado
- **Timeframe**: Persistente
- **Uso**: Pessoas, lugares, conceitos importantes
- **Vantagens**: Relacionamentos e atributos

### 4. Session Memory (Memória de Sessão)
**Propósito**: Contexto da conversa ativa
- **Storage**: In-memory + backup
- **Timeframe**: Sessão atual
- **Uso**: Fluxo natural de conversa
- **Vantagens**: Acesso instantâneo

## 🔧 Configuração

### Pré-requisitos

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Para CrewAI - OpenAI obrigatório
export OPENAI_API_KEY="sua-chave-aqui"

# 3. Para LangChain - Ollama local
ollama serve
ollama pull mistral:latest

# 4. ChromaDB é instalado automaticamente
```

### Estrutura de Dados

**CrewAI Storage Structure:**
```
05-memory/crewai_memory/
├── entities/
│   ├── chroma.sqlite3
│   └── {uuid}/
├── short_term/
│   ├── chroma.sqlite3
│   └── {uuid}/
├── long_term_memory_storage.db
└── latest_kickoff_task_outputs.db
```

**LangChain Storage Structure:**
```
05-memory/data/
├── chroma.sqlite3
└── {uuid}/
```

## 📊 Comparação das Abordagens

| Aspecto | CrewAI Memory | LangChain Memory |
|---------|---------------|------------------|
| **Complexidade** | Alta (3 tipos) | Média (1 tipo principal) |
| **Persistência** | Máxima | Boa |
| **Performance** | Otimizada | Boa |
| **Setup** | OpenAI obrigatório | Ollama local |
| **Escalabilidade** | Enterprise | Pequeno/médio |
| **Flexibilidade** | Estruturada | Flexível |
| **Interface** | CLI interativo | Web Gradio |

## 🎯 Casos de Uso

### CrewAI Memory - Ideal para:
- **Assistentes pessoais**: Relacionamentos de longo prazo
- **Customer support**: Histórico detalhado de clientes
- **Consultoria**: Projetos complexos com contexto histórico
- **Terapia/coaching**: Acompanhamento de progresso

### LangChain Memory - Ideal para:
- **Protótipos rápidos**: Testes de conceito
- **Aplicações web**: Interface visual simples
- **Multi-tenant**: Múltiplos usuários isolados
- **Desenvolvimento**: Iteração rápida

## 🔍 Monitoramento e Debug

### Verificar dados armazenados

```python
# CrewAI - Verificar memória de longo prazo
import sqlite3
conn = sqlite3.connect('05-memory/crewai_memory/long_term_memory_storage.db')
cursor = conn.execute("SELECT * FROM long_term_memory")
for row in cursor:
    print(row)

# LangChain - Verificar ChromaDB
import chromadb
client = chromadb.PersistentClient(path="05-memory/data")
collection = client.get_or_create_collection("user_conversations")
data = collection.get()
print(f"Stored documents: {len(data['documents'])}")
```

### Métricas de Qualidade

1. **Recall**: O agente lembra informações importantes?
2. **Precision**: Informações recuperadas são relevantes?
3. **Consistency**: Respostas consistentes ao longo do tempo?
4. **Personalization**: Adapta-se ao usuário específico?

## 💡 Otimizações Avançadas

### Performance
- **Embedding caching**: Cache embeddings frequentes
- **Context pruning**: Limite tamanho do contexto
- **Batch operations**: Processe múltiplas memórias juntas
- **Index optimization**: Otimize índices ChromaDB

### Qualidade
- **Memory consolidation**: Combine memórias similares
- **Importance scoring**: Priorize informações importantes
- **Conflict resolution**: Resolva informações conflitantes
- **Privacy filtering**: Remova informações sensíveis

## 🔗 Integração com outros módulos

- **02-frameworks**: Agentes com memória persistente
- **03-prompt-engineering**: Prompts conscientes de contexto
- **04-RAG**: Memória como base de conhecimento
- **06-MCP-A2A**: Compartilhamento de memória entre agentes

## 🧪 Experimentos Futuros

### Técnicas Avançadas
1. **Hierarchical Memory**: Múltiplos níveis de abstração
2. **Episodic Memory**: Lembrança de eventos específicos
3. **Semantic Memory**: Conhecimento factual estruturado
4. **Working Memory**: Contexto ativo limitado
5. **Memory Networks**: Grafos de relacionamentos

### Implementações Possíveis
- **Graph databases**: Neo4j para relacionamentos complexos
- **Vector databases**: Pinecone, Weaviate para escala
- **Distributed memory**: Redis para sistemas distribuídos
- **Compression**: Técnicas de compressão semântica