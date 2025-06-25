# 06-MCP-A2A

Esta pasta demonstra **Model Context Protocol (MCP) Agent-to-Agent** communication, mostrando como agentes de IA podem se comunicar e colaborar através de protocolos padronizados, especificamente integrando com o Context7 MCP server para análise de documentação.

## 📁 Arquivos

### `app.py`
**Interface Streamlit** para interação com agente MCP.

**Características:**
- Interface web simples e intuitiva
- Comunicação assíncrona com agente via FastMCP
- Chat persistente com histórico de mensagens
- Tratamento de erros robusto

**Funcionalidades:**
- Chat em tempo real com agente Context7
- Histórico de conversas na sessão
- Interface responsiva e amigável

### `crewai_mcp_agent.py`
**Agente CrewAI integrado com MCP Context7**

**Características:**
- **Agente Especializado**: "Elite Documentation Intelligence Analyst"
- **Integração MCP**: Conecta com Context7 server via stdio
- **CrewAI Framework**: Workflow estruturado com tarefas
- **FastMCP Server**: Expõe agente como serviço MCP

**Funcionalidades:**
- Análise inteligente de documentação técnica
- Interpretação de consultas em linguagem natural
- Extração de informações de APIs e codebases
- Geração de exemplos de código e configurações

### `langchain_mcp_agent.py`
**Agente LangChain com MCP e LangGraph**

**Características:**
- **LangGraph Workflow**: Grafo de estados para processamento
- **Múltiplos servidores MCP**: Arquitetura extensível
- **Visualização avançada**: Monitoramento step-by-step
- **Interface interativa**: Comandos especiais para debug

**Funcionalidades avançadas:**
- Visualização Mermaid do workflow
- Streaming de execução em tempo real
- Análise detalhada de estados
- Comandos de debug (`graph`, `stream`)

## 🔗 Model Context Protocol (MCP)

### O que é MCP?

**MCP** é um protocolo padronizado para comunicação entre modelos de IA e ferramentas externas, permitindo que agentes acessem e manipulem contextos de forma estruturada.

**Características principais:**
- **Protocolo aberto**: Especificação padronizada
- **Bidirectional**: Comunicação em ambas direções
- **Extensível**: Suporte a ferramentas customizadas
- **Interoperável**: Funciona entre diferentes frameworks

### Context7 Integration

**Context7** é um servidor MCP especializado em análise de documentação:
- **NPM Package**: `@upstash/context7-mcp`
- **Funcionalidades**: Busca e análise de documentação
- **Transporte**: stdio (standard input/output)
- **Uso**: Consultas de documentação técnica

## 🚀 Como usar

### 1. Pré-requisitos

```bash
# 1. Instalar dependências Python
pip install -r requirements.txt

# 2. Instalar Node.js (para Context7)
# Download: https://nodejs.org

# 3. Configurar OpenAI API
export OPENAI_API_KEY="sua-chave-aqui"

# 4. Verificar NPX está disponível
npx --version
```

### 2. CrewAI MCP Agent

```bash
# Iniciar servidor MCP com agente CrewAI
python crewai_mcp_agent.py

# Servidor fica disponível em:
# http://127.0.0.1:8004/sse
```

**Em outro terminal:**
```bash
# Iniciar interface Streamlit
streamlit run app.py
```

### 3. LangChain MCP Agent

```bash
# Executar agente LangChain interativo
python langchain_mcp_agent.py
```

**Comandos especiais:**
- `graph`: Visualizar estrutura do workflow
- `stream <pergunta>`: Executar com monitoramento detalhado
- `quit`: Sair do agente

## 🔧 Arquitetura MCP

### CrewAI Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastMCP       │    │   Context7      │
│   Interface     │───▶│   Server        │───▶│   MCP Server    │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ User Input  │ │    │ │ CrewAI      │ │    │ │ NPX Process │ │
│ │ Chat UI     │ │    │ │ Agent       │ │    │ │ stdio       │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### LangChain Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph Workflow                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐     ┌──────────┐     ┌──────────────────────┐ │
│  │  START   │────▶│call_model│────▶│   tools_condition    │ │
│  └──────────┘     └──────────┘     └──────────────────────┘ │
│                                     │                      │ │
│  ┌──────────┐     ┌──────────┐     │                      │ │
│  │   END    │◀────│  tools   │◀────┘                      │ │
│  └──────────┘     └──────────┘                            │ │
├─────────────────────────────────────────────────────────────┤
│                 MultiServerMCPClient                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Context7: npx @upstash/context7-mcp                   │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Comparação das Abordagens

| Aspecto | CrewAI MCP | LangChain MCP |
|---------|------------|---------------|
| **Complexidade** | Baixa | Alta |
| **Interface** | Web (Streamlit) | CLI Interativo |
| **Workflow** | Sequencial simples | Grafo de estados |
| **Monitoramento** | Básico | Avançado |
| **Extensibilidade** | Média | Alta |
| **Visualização** | Nenhuma | Mermaid + Streaming |
| **Debug** | Logs básicos | Step-by-step |
| **Deploy** | Fácil (web app) | Desenvolvimento |

## 🎯 Funcionalidades Demonstradas

### Context7 Capabilities

**Tipos de consultas suportadas:**
- Busca em documentação de APIs
- Análise de codebases
- Explicação de conceitos técnicos
- Geração de exemplos de uso
- Configuração de ferramentas

**Exemplos de perguntas:**
```
"Find documentation for React hooks"
"How to configure FastAPI with async?"
"What is the Context7 MCP protocol?"
"Show me examples of LangChain agents"
```

### LangGraph Features

**Visualização e Monitoramento:**
- **Mermaid Diagrams**: Representação visual do workflow
- **Step-by-step Execution**: Acompanhamento em tempo real
- **State Inspection**: Análise detalhada de estados
- **Tool Call Tracking**: Monitoramento de chamadas de ferramentas

## 🔍 Debugging e Desenvolvimento

### Logs e Monitoramento

**CrewAI Debugging:**
```python
# Habilitar logs verbosos
agent = Agent(verbose=True, ...)
crew = Crew(verbose=True, ...)
```

**LangChain Debugging:**
```python
# Streaming de eventos
async for event in graph.astream(input_data):
    print(f"Node: {list(event.keys())[0]}")
    # Processar evento...
```

### Tratamento de Erros

**Problemas comuns:**
1. **NPX não encontrado**: Instalar Node.js
2. **Context7 timeout**: Verificar conectividade de rede
3. **OpenAI API**: Verificar chave e limites
4. **MCP Connection**: Verificar processo stdio

**Soluções:**
```bash
# Verificar NPX
which npx

# Testar Context7 manualmente
npx @upstash/context7-mcp

# Debug de conexão MCP
export MCP_DEBUG=1
python crewai_mcp_agent.py
```

## 💡 Casos de Uso

### Ideal para MCP Agent-to-Agent:

1. **Análise de Documentação**:
   - APIs complexas
   - Frameworks e bibliotecas
   - Configurações técnicas

2. **Consultoria Técnica**:
   - Troubleshooting
   - Best practices
   - Architecture guidance

3. **Desenvolvimento Assistido**:
   - Code generation
   - Configuration templates
   - Integration examples

4. **Knowledge Management**:
   - Technical wikis
   - Process documentation
   - Training materials

## 🔗 Extensões e Integrações

### Outros Servidores MCP

**Exemplos de integração:**
```python
# Múltiplos servidores MCP
client = MultiServerMCPClient({
    "context7": {
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp"]
    },
    "filesystem": {
        "command": "mcp-server-filesystem",
        "args": ["/path/to/docs"]
    },
    "database": {
        "command": "mcp-server-sqlite",
        "args": ["database.db"]
    }
})
```

### Custom MCP Servers

**Criar servidor MCP customizado:**
```python
from fastmcp import FastMCP

mcp = FastMCP("custom-server")

@mcp.tool()
async def custom_tool(query: str) -> str:
    # Implementar funcionalidade customizada
    return "Custom response"

if __name__ == "__main__":
    mcp.run()
```

## 🧪 Experimentos Futuros

### Técnicas Avançadas

1. **Multi-Agent MCP**:
   - Agentes especializados
   - Orquestração distribuída
   - Load balancing

2. **MCP Chaining**:
   - Pipeline de servidores
   - Transformação de dados
   - Workflows complexos

3. **Hybrid Architectures**:
   - Local + Remote MCP
   - Cache intelligent
   - Fallback strategies

4. **Security & Privacy**:
   - Authentication
   - Data encryption
   - Audit logging

## 📚 Conceitos Demonstrados

- **Protocol standardization**: MCP como padrão de comunicação
- **Agent orchestration**: Coordenação entre agentes
- **Tool integration**: Integração transparente de ferramentas
- **Asynchronous processing**: Comunicação assíncrona
- **State management**: Gestão de estado complexo
- **Workflow visualization**: Monitoramento visual
- **Error handling**: Tratamento robusto de erros
- **Scalable architecture**: Arquitetura extensível

## 🔗 Integração com outros módulos

- **02-frameworks**: MCP como middleware entre frameworks
- **03-prompt-engineering**: Prompts especializados para MCP
- **04-RAG**: MCP servers como fontes de conhecimento
- **05-memory**: Compartilhamento de memória via MCP