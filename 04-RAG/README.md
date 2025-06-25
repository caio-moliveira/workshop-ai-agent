# 04-RAG

Esta pasta contém uma implementação completa de **Retrieval-Augmented Generation (RAG)**, demonstrando cada etapa do processo desde o carregamento de documentos até a geração de respostas contextuais.

## 📁 Arquivos

### `RAG_simples.py`
**Sistema RAG completo e minimalista** em um único arquivo.

**Pipeline completo:**
1. **Processamento**: Carregamento de PDF
2. **Chunking**: Divisão em chunks com overlap
3. **Embeddings**: Conversão para vetores
4. **Busca**: Pesquisa semântica
5. **Contexto**: Enriquecimento de contexto
6. **Geração**: Resposta final

**Características:**
- Suporte Ollama local + OpenAI opcional
- Interface simples e educativa
- Download automático de dados de exemplo
- Pipeline demonstrativo passo a passo

### `chunking-example.py`
**Demonstração detalhada do Step 2: Text Chunking**

**Funcionalidades:**
- Análise de parâmetros de chunking (tamanho, overlap)
- Estatísticas detalhadas dos chunks
- Visualização de amostras
- Análise de qualidade das divisões
- Detecção de limites limpos vs cortados

### `embedding-example.py`
**Demonstração do Step 3: Creating Embeddings**

**Funcionalidades:**
- Criação de embeddings com Ollama
- Análise de propriedades dos vetores
- Comparação de similaridade entre textos
- Demonstração de busca vetorial básica
- Métricas de similaridade cosine

### `semantic-search-example.py`
**Demonstração do Step 4: Semantic Search**

**Funcionalidades:**
- Busca semântica vs busca por palavras-chave
- Comparação de diferentes parâmetros de busca
- Demonstração de scores de similaridade
- Busca interativa
- Análise de relevância dos resultados

### `context_enrichment.py`
**Demonstração do Step 5: Context Enrichment**

**Funcionalidades:**
- Combinação de múltiplos chunks recuperados
- Análise de qualidade do contexto
- Comparação de diferentes tamanhos de contexto
- Métricas de relevância e completude
- Preparação para geração de respostas

### `evaluate-RAG.py`
**Sistema de avaliação de performance RAG**

**Métricas de avaliação:**
- **Correctness**: Precisão factual das respostas
- **Faithfulness**: Fidelidade ao contexto recuperado
- **Contextual Relevancy**: Relevância do contexto recuperado
- **GEval**: Avaliação customizada com GPT-4

**Funcionalidades:**
- Criação de casos de teste estruturados
- Avaliação automatizada com deepeval
- Geração de métricas quantitativas
- Análise comparativa de performance

### `data/Understanding_Climate_Change.pdf`
**Documento de exemplo** sobre mudanças climáticas para demonstrações.

## 🚀 Como usar

### 1. RAG Completo (Recomendado para iniciantes)

```bash
# Executar sistema RAG completo
python RAG_simples.py

# Opções durante execução:
# - Usar apenas Ollama (gratuito, local)
# - Usar Ollama + OpenAI (embedding local + geração OpenAI)
```

### 2. Explorando etapas individuais

```bash
# Step 2: Chunking
python chunking-example.py

# Step 3: Embeddings
python embedding-example.py

# Step 4: Semantic Search
python semantic-search-example.py

# Step 5: Context Enrichment
python context_enrichment.py
```

### 3. Avaliação de performance

```bash
# Avaliar sistema RAG
python evaluate-RAG.py
```

## 🎯 Pipeline RAG Detalhado

### Step 1: Document Processing
```
PDF → Text Extraction → Metadata Preservation
```

### Step 2: Text Chunking
```
Large Text → Smart Splitting → Overlapped Chunks
```
**Parâmetros importantes:**
- `chunk_size`: Tamanho dos chunks (recomendado: 500-1500 chars)
- `chunk_overlap`: Sobreposição (recomendado: 10-20% do chunk_size)

### Step 3: Creating Embeddings
```
Text Chunks → Vector Embeddings → Vector Store (FAISS)
```
**Modelo usado**: `mxbai-embed-large:latest` (Ollama)

### Step 4: Semantic Search
```
Query → Query Embedding → Similarity Search → Relevant Chunks
```
**Métricas**: Similaridade cosine (menor score = maior relevância)

### Step 5: Context Enrichment
```
Retrieved Chunks → Context Combination → Quality Analysis
```

### Step 6: Answer Generation
```
Query + Context → LLM → Final Answer
```

## 📊 Configuração e Otimização

### Pré-requisitos

```bash
# 1. Instalar Ollama
# Download: https://ollama.ai
ollama serve
ollama pull mxbai-embed-large:latest
ollama pull mistral:latest  # ou deepseek-r1:8b

# 2. Instalar dependências Python
pip install -r requirements.txt

# 3. (Opcional) Configurar OpenAI
export OPENAI_API_KEY="sua-chave-aqui"
```

### Parâmetros de Otimização

| Parâmetro | Valor Recomendado | Impacto |
|-----------|-------------------|---------|
| `chunk_size` | 1000 chars | Balanço contexto/precisão |
| `chunk_overlap` | 200 chars | Continuidade informação |
| `k` (retrieval) | 3-5 chunks | Contexto suficiente |
| `temperature` | 0-0.3 | Precisão vs criatividade |

### Modelo Embeddings

**mxbai-embed-large:latest** (Ollama)
- Dimensões: 1024
- Idioma: Multilingual
- Performance: Alta qualidade
- Velocidade: Local, sem API

## 🔍 Análise de Performance

### Métricas de Avaliação

1. **Retrieval Metrics**:
   - Precision@k: Precisão dos top-k resultados
   - Recall@k: Cobertura dos resultados relevantes
   - MRR: Mean Reciprocal Rank

2. **Generation Metrics**:
   - BLEU: Similaridade com respostas de referência
   - ROUGE: Overlap de n-gramas
   - BERTScore: Similaridade semântica

3. **End-to-End Metrics**:
   - Correctness: Precisão factual
   - Faithfulness: Fidelidade ao contexto
   - Relevancy: Relevância contextual

### Debugging RAG

**Problemas comuns:**

1. **Chunks irrelevantes**:
   - Ajustar chunk_size/overlap
   - Melhorar query reformulation
   - Usar reranking

2. **Contexto insuficiente**:
   - Aumentar k (número de chunks)
   - Melhorar estratégia de chunking
   - Context enrichment

3. **Respostas inconsistentes**:
   - Reduzir temperature
   - Melhorar prompt engineering
   - Usar self-consistency

## 💡 Casos de Uso

### Ideais para RAG
- **Documentação técnica**: Manuais, APIs, guias
- **Base de conhecimento**: FAQ, policies, procedures
- **Pesquisa acadêmica**: Papers, relatórios, estudos
- **Conteúdo empresarial**: Relatórios, apresentações

### Limitações
- **Informações desatualizadas**: RAG é estático
- **Raciocínio complexo**: Melhor usar fine-tuning
- **Dados estruturados**: Consider SQL/GraphRAG
- **Tempo real**: Informações dinâmicas

## 🧪 Experimentos e Extensões

### Técnicas Avançadas (não implementadas aqui)

1. **Advanced Chunking**:
   - Semantic chunking
   - Sliding window
   - Document-aware splitting

2. **Retrieval Enhancement**:
   - Hybrid search (keyword + semantic)
   - Reranking models
   - Query expansion

3. **Context Optimization**:
   - Context compression
   - Relevant sentence extraction
   - Multi-hop reasoning

4. **Evaluation**:
   - Human evaluation
   - A/B testing
   - Domain-specific metrics

## 🔗 Integração com outros módulos

- **02-frameworks**: RAG como ferramenta para agentes
- **03-prompt-engineering**: Otimização de prompts RAG
- **05-memory**: RAG como sistema de memória externa
- **06-MCP-A2A**: RAG via Model Context Protocol

## 📚 Conceitos Demonstrados

- **Vector databases**: FAISS para busca eficiente
- **Embedding models**: Representação semântica
- **Similarity search**: Recuperação por significado
- **Context window management**: Otimização de contexto
- **Evaluation frameworks**: Métricas de qualidade
- **Local vs cloud**: Ollama local vs OpenAI