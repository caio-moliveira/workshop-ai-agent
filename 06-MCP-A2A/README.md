# 🔗 06-MCP-A2A - Model Context Protocol Agent-to-Agent

Esta pasta demonstra **Model Context Protocol (MCP) Agent-to-Agent** communication, mostrando como agentes de IA podem se comunicar e colaborar através de protocolos padronizados. Inclui implementações com **CrewAI**, **LangChain**, e **LangGraph** integradas ao **Context7 MCP server** para análise inteligente de documentação.

## 🎯 Objetivo

Demonstrar na prática:
- **Comunicação inter-agentes** via protocolos padronizados
- **Integração MCP** com diferentes frameworks de IA
- **Colaboração estruturada** entre agentes especializados
- **Orquestração** de workflows multi-agente
- **Observabilidade** e debugging de sistemas distribuídos

## 📁 Arquitetura dos Projetos

### 🚀 Projetos Implementados

| Arquivo | Framework | Complexidade | Interface | Foco |
|---------|-----------|--------------|-----------|------|
| **`crewai_mcp_agent.py`** + **`app.py`** | CrewAI | ⭐⭐ | Web (Streamlit) | Produção |
| **`lang_mcp_agent.py`** | LangChain | ⭐⭐⭐ | CLI Interativo | Desenvolvimento |
| **`a2a_langgraph.py`** | LangGraph | ⭐⭐⭐⭐ | CLI + Visualização | Pesquisa |

## 🏗️ Implementações Detalhadas

### 1. 🎨 CrewAI MCP Agent (Produção Ready)

**Arquitetura:**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastMCP       │    │   Context7      │
│   Interface     │───▶│   Server        │───▶│   MCP Server    │
│   (app.py)      │    │ (crewai_agent)  │    │   (NPX/Node)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Características:**
- **Agente Especializado**: "Elite Documentation Intelligence Analyst"
- **Web Interface**: Interface Streamlit responsiva e intuitiva
- **FastMCP Server**: Expõe agente CrewAI como serviço MCP
- **Chat Persistente**: Histórico de conversas na sessão
- **Tratamento de Erros**: Fallback e recovery robusto

**Como usar:**
```bash
# Terminal 1: Iniciar servidor MCP
python crewai_mcp_agent.py
# Servidor disponível em: http://127.0.0.1:8004/sse

# Terminal 2: Interface web
streamlit run app.py
# Interface disponível em: http://localhost:8501
```

### 2. ⚡ LangChain MCP Agent (Desenvolvimento)

**Arquitetura:**
```
┌─────────────────────────────────────────────────────────────┐
│                 LangChain MCP Client                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐     ┌─────────────────────────────────┐   │
│  │ ChatOpenAI   │────▶│   create_react_agent           │   │
│  │ (gpt-4o-mini)│     │   (ReAct Pattern)              │   │
│  └──────────────┘     └─────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│                 MCP Tools Integration                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Context7: npx @upstash/context7-mcp@latest            │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Características:**
- **ReAct Pattern**: Reasoning + Acting em loop
- **Tool Integration**: Integração automática de ferramentas MCP
- **Session Management**: Gestão de sessão com Context7
- **CLI Interativo**: Interface de linha de comando rica

**Como usar:**
```bash
# Executar agente interativo
python lang_mcp_agent.py

# Comandos disponíveis:
# - Perguntas diretas sobre documentação
# - "quit" para sair
```

### 3. 🧩 LangGraph Multi-Agent (Avançado)

**Arquitetura:**
```
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph Workflow                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐     ┌──────────┐     ┌──────────────────────┐ │
│  │  START   │────▶│Researcher│────▶│   Writer Agent      │ │
│  │          │     │Agent     │     │                      │ │
│  │          │     │(Tavily+  │     │ (GPT Analysis +      │ │
│  │          │     │ GPT)     │     │  Article Creation)   │ │
│  └──────────┘     └──────────┘     └──────────────────────┘ │
│                                     │                      │ │
│  ┌──────────┐                      │                      │ │
│  │   END    │◀─────────────────────┘                      │ │
│  └──────────┘                                             │ │
└─────────────────────────────────────────────────────────────┘
```

**Características:**
- **Estado Compartilhado**: TypedDict com informações entre agentes
- **Researcher Agent**: Busca web (Tavily) + análise LLM
- **Writer Agent**: Criação de artigos baseada em pesquisa
- **Workflow Visual**: Grafo de estados observável
- **Fallback Strategy**: LLM-only se APIs externas falharem

**Como usar:**
```bash
# Configurar APIs (opcionais)
export OPENAI_API_KEY="sua-chave"
export TAVILY_API_KEY="sua-chave"  # Web search

# Executar workflow
python a2a_langgraph.py
```

## 🔧 Model Context Protocol (MCP)

### 🌐 O que é MCP?

**MCP** é um protocolo aberto que permite comunicação estruturada entre modelos de IA e ferramentas externas, criando um ecossistema interoperável de agentes.

**Principais Características:**
- **🔄 Protocolo Bidirecional**: Comunicação em ambas direções
- **📡 Transport Agnostic**: stdio, HTTP, WebSocket
- **🔧 Tool Integration**: Ferramentas como funções nativas
- **📋 Standardized**: Especificação aberta e padronizada
- **🔗 Interoperable**: Funciona entre diferentes frameworks

### 🛠️ Context7 Integration

**Context7** é um servidor MCP especializado em análise de documentação:

| Aspecto | Detalhes |
|---------|----------|
| **Package** | `@upstash/context7-mcp@latest` |
| **Transport** | stdio (Standard Input/Output) |
| **Funcionalidades** | Busca e análise de documentação técnica |
| **Compatibilidade** | Multiplataforma via NPX |
| **Performance** | Otimizado para consultas técnicas |

**Exemplo de uso:**
```bash
# Testar Context7 diretamente
npx -y @upstash/context7-mcp@latest

# Integração programática
server_params = StdioServerParameters(
    command="npx",
    args=["-y", "@upstash/context7-mcp@latest"]
)
```

## 🚀 Configuração e Instalação

### 1. 📋 Pré-requisitos

```bash
# 1. Node.js (para Context7)
# Download: https://nodejs.org
node --version  # Verificar instalação
npx --version   # Verificar NPX

# 2. Python 3.8+
python --version

# 3. APIs (opcionais)
export OPENAI_API_KEY="sua-chave-openai"
export TAVILY_API_KEY="sua-chave-tavily"  # Para busca web
```

### 2. 📦 Dependências Python

```bash
# Instalar dependências
pip install -r requirements.txt

# Principais bibliotecas instaladas:
# - crewai, crewai-tools[mcp]
# - langchain, langgraph, langchain-mcp-adapters
# - fastmcp, mcp
# - streamlit
# - openai
```

### 3. 🔧 Verificação da Configuração

```bash
# Testar Context7
npx -y @upstash/context7-mcp@latest

# Verificar APIs
python -c "import openai; print('OpenAI OK')"
python -c "import streamlit; print('Streamlit OK')"
```

## 📊 Comparação das Abordagens

| Aspecto | CrewAI | LangChain | LangGraph |
|---------|--------|-----------|-----------|
| **🏗️ Complexidade** | Baixa | Média | Alta |
| **🖥️ Interface** | Web (Streamlit) | CLI | CLI + Visuals |
| **🔄 Workflow** | Sequencial | ReAct Loop | Estado/Grafo |
| **📊 Observabilidade** | Logs básicos | Session tracking | Visual + Streaming |
| **🔧 Extensibilidade** | Média | Alta | Muito Alta |
| **🚀 Deploy** | Produção ready | Desenvolvimento | Pesquisa/Prototipo |
| **📈 Learning Curve** | Fácil | Média | Avançada |
| **🎯 Melhor para** | MVPs rápidos | Integrações | Workflows complexos |

## 💡 Casos de Uso Práticos

### 🎯 Ideais para MCP A2A

1. **📚 Análise de Documentação**
   ```
   Cenário: Desenvolvedor quer entender API complexa
   Solução: Context7 + Agent análise → Explicação + Exemplos
   ```

2. **🔍 Consultoria Técnica**
   ```
   Cenário: Troubleshooting de configuração
   Solução: Agent busca docs → Agent analisa → Agent responde
   ```

3. **⚡ Desenvolvimento Assistido**
   ```
   Cenário: Gerar código específico para biblioteca
   Solução: Context7 docs → Code generation → Validation
   ```

4. **🧠 Knowledge Management**
   ```
   Cenário: Onboarding de novos desenvolvedores
   Solução: Agent guia → Context search → Learning path
   ```

### 📝 Exemplos de Perguntas

**Para Context7:**
```
"How to configure FastAPI with async database?"
"Find React hooks documentation and examples"
"What are LangChain memory components?"
"Show me Context7 MCP protocol usage"
"Explain CrewAI multi-agent workflows"
```

**Para LangGraph Multi-Agent:**
```
"Research and write about quantum computing applications"
"Analyze trends in sustainable energy and create report"
"Investigate blockchain scalability solutions"
```

## 🔍 Debugging e Observabilidade

### 🐛 Debugging CrewAI

```python
# Habilitar logs detalhados
agent = Agent(
    verbose=True,     # Logs de agente
    # ... outras configurações
)

crew = Crew(
    verbose=True,     # Logs de execução
    # ... outras configurações
)

# Logs MCP
os.environ["MCP_DEBUG"] = "1"
```

### 🔬 Debugging LangChain

```python
# Callback para observabilidade
from langchain.callbacks import StdOutCallbackHandler

callbacks = [StdOutCallbackHandler()]
agent = create_react_agent(model, tools, callbacks=callbacks)

# Debug de sessão MCP
async with ClientSession(read, write) as session:
    await session.initialize()
    print(f"Available tools: {[tool.name for tool in tools]}")
```

### 📊 Debugging LangGraph

```python
# Streaming de execução
async for event in graph.astream(input_data):
    node_name = list(event.keys())[0]
    node_data = event[node_name]
    print(f"📍 Node: {node_name}")
    print(f"📊 Data: {node_data}")

# Visualização do grafo
graph.get_graph().print_ascii()
```

### ⚠️ Problemas Comuns e Soluções

| Problema | Sintoma | Solução |
|----------|---------|---------|
| **NPX não encontrado** | `command not found: npx` | Instalar Node.js |
| **Context7 timeout** | `Connection timeout` | Verificar conectividade |
| **OpenAI API Error** | `401 Unauthorized` | Verificar `OPENAI_API_KEY` |
| **MCP Connection** | `stdio connection failed` | Verificar processo NPX |
| **Streamlit Error** | `ModuleNotFoundError` | `pip install streamlit` |

```bash
# Script de diagnóstico
echo "🔍 Diagnóstico MCP A2A"
echo "Node.js: $(node --version 2>/dev/null || echo 'FALTANDO')"
echo "NPX: $(npx --version 2>/dev/null || echo 'FALTANDO')"
echo "Context7: $(npx -y @upstash/context7-mcp@latest --help 2>/dev/null | head -1 || echo 'ERRO')"
echo "OpenAI: ${OPENAI_API_KEY:0:10}... $([ -n "$OPENAI_API_KEY" ] && echo 'OK' || echo 'FALTANDO')"
```

## 🔬 Extensões e Experimentos

### 🚀 Múltiplos Servidores MCP

```python
# Configuração multi-servidor
servers = {
    "context7": {
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "filesystem": {
        "command": "mcp-server-filesystem", 
        "args": ["/path/to/docs"]
    },
    "database": {
        "command": "mcp-server-sqlite",
        "args": ["knowledge.db"]
    }
}
```

### 🧪 Custom MCP Server

```python
from fastmcp import FastMCP

# Servidor MCP customizado
mcp = FastMCP("custom-knowledge-server")

@mcp.tool()
async def knowledge_search(query: str, domain: str) -> str:
    """Busca conhecimento em domínio específico"""
    # Implementar lógica customizada
    return f"Knowledge about {query} in {domain}"

@mcp.tool() 
async def code_analysis(code: str, language: str) -> str:
    """Analisa código fonte"""
    # Implementar análise de código
    return f"Analysis of {language} code"

if __name__ == "__main__":
    mcp.run(transport="sse", port=8005)
```

### 🔗 Integração Avançada

```python
# Pipeline multi-agente com MCP
class AdvancedMCPPipeline:
    def __init__(self):
        self.context7 = self._init_context7()
        self.custom_server = self._init_custom()
        self.orchestrator = self._init_orchestrator()
    
    async def process_complex_query(self, query: str):
        # 1. Análise inicial com Context7
        context = await self.context7.search(query)
        
        # 2. Processamento customizado
        analysis = await self.custom_server.analyze(context)
        
        # 3. Orquestração final
        result = await self.orchestrator.synthesize(analysis)
        
        return result
```

## 🏆 Resultados de Aprendizado

Após completar este módulo, você será capaz de:

### 🎯 Conceitos Fundamentais
✅ **Compreender** protocolos de comunicação inter-agentes  
✅ **Implementar** agentes MCP com diferentes frameworks  
✅ **Orquestrar** workflows multi-agente complexos  
✅ **Debuggar** sistemas distribuídos de IA  

### 🛠️ Habilidades Técnicas
✅ **Integrar** Context7 MCP com CrewAI/LangChain/LangGraph  
✅ **Criar** interfaces web e CLI para agentes  
✅ **Configurar** servidores MCP customizados  
✅ **Monitorar** execução de workflows com observabilidade  

### 🚀 Aplicações Práticas
✅ **Desenvolver** assistentes de documentação inteligentes  
✅ **Construir** sistemas de consultoria técnica automatizada  
✅ **Implementar** pipelines de análise de conhecimento  
✅ **Escalar** soluções para múltiplos domínios  

## 🔮 Técnicas Futuras e Pesquisa

### 🧪 Experimentação Avançada

1. **🌐 Multi-Protocol Integration**
   ```python
   # Combinação MCP + WebSocket + HTTP
   hybrid_agent = HybridProtocolAgent([
       MCPConnection("context7"),
       WebSocketConnection("realtime-data"),
       HTTPConnection("external-api")
   ])
   ```

2. **🔄 Agent Chaining**
   ```python
   # Cadeia de processamento
   chain = AgentChain([
       ResearchAgent(mcp="context7"),
       AnalysisAgent(mcp="custom-analyzer"), 
       SynthesisAgent(mcp="knowledge-base"),
       ValidationAgent(mcp="fact-checker")
   ])
   ```

3. **🎛️ Dynamic Orchestration**
   ```python
   # Orquestração adaptativa
   orchestrator = DynamicOrchestrator()
   orchestrator.add_strategy("technical_docs", context7_strategy)
   orchestrator.add_strategy("business_analysis", multi_agent_strategy)
   orchestrator.auto_route(query)
   ```

### 🔬 Áreas de Pesquisa

- **Performance Optimization**: Cache inteligente, lazy loading
- **Security & Privacy**: Autenticação, criptografia de dados
- **Fault Tolerance**: Recovery automático, circuit breakers
- **Scalability**: Load balancing, distributed processing
- **Interoperability**: Cross-platform, cross-protocol

## 📚 Recursos Adicionais

### 📖 Documentação Oficial
- **MCP Specification**: https://modelcontextprotocol.io/
- **Context7 Docs**: https://context7.upstash.com/
- **CrewAI Docs**: https://docs.crewai.com/
- **LangChain MCP**: https://python.langchain.com/docs/integrations/tools/mcp/
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/

### 🎥 Recursos de Aprendizado
- **MCP Protocol Deep Dive**: Specifications e exemplos
- **Agent Communication Patterns**: Melhores práticas
- **Debugging Distributed Systems**: Técnicas avançadas
- **Performance Tuning**: Otimização de workflows

### 🛠️ Ferramentas Complementares
- **MCP Inspector**: Debug visual de protocolos
- **Agent Monitor**: Observabilidade de agentes
- **Workflow Visualizer**: Grafos de execução
- **Performance Profiler**: Análise de performance

## 🤝 Contribuição e Desenvolvimento

### 🔧 Desenvolvimento Local

```bash
# Setup desenvolvimento
git clone <seu-repo>
cd 06-MCP-A2A

# Ambiente virtual
python -m venv .venv
source .venv/bin/activate

# Dependências development
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Testes
pytest tests/
```

### 📝 Estrutura de Contribuição

```
06-MCP-A2A/
├── tests/                    # Testes automatizados
│   ├── test_crewai_agent.py
│   ├── test_langchain_agent.py
│   └── test_langgraph_workflow.py
├── docs/                     # Documentação adicional
│   ├── architecture.md
│   ├── deployment.md
│   └── troubleshooting.md
├── examples/                 # Exemplos adicionais
│   ├── custom_mcp_server.py
│   ├── multi_server_setup.py
│   └── production_config.py
└── utils/                    # Utilitários compartilhados
    ├── mcp_helpers.py
    ├── logging_config.py
    └── performance_monitor.py
```

### 🎯 Roadmap de Melhorias

- [ ] **Interface Gráfica**: Dashboard para monitoramento
- [ ] **Métricas Avançadas**: Performance e qualidade
- [ ] **Templates**: Configurações pré-definidas
- [ ] **CI/CD**: Pipeline de deployment automático
- [ ] **Docker**: Containerização completa
- [ ] **Kubernetes**: Orquestração em cluster

---

## 🎉 Conclusão

Este módulo demonstra como **Model Context Protocol** revoluciona a comunicação entre agentes de IA, criando sistemas:

🌟 **Interoperáveis** - Protocolos padronizados  
🌟 **Escaláveis** - Arquitetura distribuída  
🌟 **Observáveis** - Monitoramento completo  
🌟 **Extensíveis** - Fácil adição de novos agentes  

**🚀 Próximos Passos:** 
- Explore **04-RAG** para ver como integrar conhecimento via MCP
- Experimente criar seus próprios servidores MCP customizados
- Combine multiple frameworks para workflows híbridos

---

**💡 Dica:** Comece com **CrewAI** para protótipos rápidos, evolua para **LangChain** para integrações, e use **LangGraph** para workflows complexos!