# 03-prompt-engineering

Esta pasta demonstra técnicas avançadas de **Prompt Engineering** para otimizar a qualidade e eficácia de respostas de modelos de linguagem, com exemplos práticos e uma aplicação completa de análise de currículos.

## 📁 Arquivos

### `app.py`
**Aplicação Streamlit** para análise inteligente de currículos e vagas.

**Funcionalidades:**
- Upload de PDF (currículo e descrição da vaga)
- Dois modos de operação:
  - **Modo Contratação**: Análise para recrutadores
  - **Modo Candidato**: Feedback para melhorar currículo
- Análise de compatibilidade com pontuação
- Geração de sugestões personalizadas
- Reescrita automática de currículo melhorado

**Características técnicas:**
- Interface web responsiva
- Processamento de PDF com PyMuPDF
- Pipeline de análise com LangChain
- Integração com Ollama (Mistral)

### `prompts.py`
**Biblioteca de prompts especializados** para diferentes etapas da análise.

**Prompts incluídos:**
- `JD_PARSING_PROMPT`: Extração estruturada de requisitos da vaga
- `RESUME_PARSING_PROMPT`: Análise de currículo em formato padronizado
- `EVALUATION_PROMPT`: Avaliação de compatibilidade com scoring
- `SUGGESTIONS_PROMPT`: Geração de melhorias direcionadas
- `CV_REWRITE_PROMPT`: Reescrita otimizada para ATS

### `scripts.py`
**Engine de processamento** com pipelines LangChain.

**Funcionalidades:**
- `AI_Utilities`: Classe principal de processamento
- Análise paralela de documentos
- Avaliação JSON estruturada
- Geração de relatórios em Markdown
- Limpeza e validação de saídas

### `tecnica_basica.py`
**Demonstração de técnicas fundamentais** de prompt engineering.

**Técnicas abordadas:**
- **Zero-Shot**: Pergunta direta sem contexto
- **Few-Shot**: Aprendizado por exemplos
- **Chain of Thought**: Raciocínio passo a passo
- **Role Prompting**: Assumir papel de especialista

**Cenário único**: Análise de produto e-commerce para demonstrar como diferentes técnicas geram resultados distintos.

### `tecnica_avancada.py`
**Técnicas sofisticadas** para casos complexos.

**Técnicas demonstradas:**
- **Self-Consistency**: Múltiplas execuções para confiabilidade
- **Tree of Thoughts**: Exploração de múltiplos caminhos
- **Prompt Chaining**: Quebra de problemas complexos em etapas
- **Structured Output**: Saídas em formato JSON estruturado
- **Negative Prompting**: Especificação do que evitar

**Cenário único**: Estratégia de marketing para startup para mostrar a diferença entre abordagens.

## 🚀 Como usar

### 1. Aplicação de Análise de Currículos

```bash
# Iniciar aplicação web
streamlit run app.py
```

**Fluxo de uso:**
1. Selecionar modo (Contratação/Candidato)
2. Upload PDF da vaga e currículo
3. Receber análise automática
4. Obter sugestões de melhoria
5. Gerar currículo otimizado (modo candidato)

### 2. Técnicas Básicas

```bash
# Demonstrar técnicas fundamentais
python tecnica_basica.py
```

**O que demonstra:**
- Como diferentes prompts afetam o resultado
- Comparação lado a lado das técnicas
- Guia de quando usar cada abordagem

### 3. Técnicas Avançadas

```bash
# Demonstrar técnicas sofisticadas
python tecnica_avancada.py
```

**O que demonstra:**
- Otimizações para problemas complexos
- Técnicas de validação e consistência
- Estruturação de saídas complexas

## 🎯 Técnicas de Prompt Engineering

### Básicas

| Técnica | Uso | Vantagens | Limitações |
|---------|-----|-----------|------------|
| **Zero-Shot** | Tarefas simples | Rápido, direto | Pode ser vago |
| **Few-Shot** | Formato específico | Consistente | Prompt longo |
| **Chain of Thought** | Raciocínio complexo | Transparente | Verboso |
| **Role Prompting** | Expertise específica | Profundo | Pode ser limitado |

### Avançadas

| Técnica | Uso | Vantagens | Limitações |
|---------|-----|-----------|------------|
| **Self-Consistency** | Alta confiabilidade | Reduz variação | 3x mais tokens |
| **Tree of Thoughts** | Múltiplas soluções | Abrangente | Resposta extensa |
| **Prompt Chaining** | Problemas complexos | Estruturado | Múltiplas chamadas |
| **Structured Output** | Dados estruturados | Fácil integração | Pode ser rígido |
| **Negative Prompting** | Evitar problemas | Mais focado | Prompt maior |

## 📊 Aplicação Prática: Análise de Currículos

### Pipeline de Processamento

```
PDF Upload → Parsing → Análise Paralela → Avaliação → Sugestões → Reescrita
```

### Componentes Principais

1. **Extração de Dados**: PDF → Texto estruturado
2. **Análise Paralela**: Vaga + Currículo simultaneamente
3. **Scoring Inteligente**: Pontuação baseada em critérios
4. **Sugestões Direcionadas**: Melhorias específicas
5. **Reescrita Otimizada**: ATS-friendly

### Métricas de Avaliação

- **Pontuação Geral**: 0-100
- **Penalidades**: Superqualificação, lacunas críticas
- **Pontos Positivos**: Correspondências exatas
- **Lacunas**: Requisitos não atendidos
- **Recomendação**: Prosseguir/Rejeitar

## 🔧 Configuração

### Pré-requisitos

```bash
# Instalar Ollama
ollama serve
ollama pull mistral:latest

# Instalar dependências
pip install -r requirements.txt
```

### Variáveis de Ambiente (Opcional)

```bash
# Para usar OpenAI em vez de Ollama
export OPENAI_API_KEY="sua-chave-aqui"
```

## 💡 Boas Práticas

### Prompt Design
- **Seja específico**: Detalhe exatamente o que deseja
- **Use exemplos**: Few-shot para formatos consistentes
- **Estruture saídas**: JSON para processamento automático
- **Teste variações**: Self-consistency para validação
- **Especifique restrições**: Negative prompting para evitar problemas

### Otimização
- **Escolha a técnica certa**: Baseado na complexidade
- **Combine técnicas**: Mix para melhores resultados
- **Monitore tokens**: Balance qualidade vs custo
- **Valide saídas**: Estruturas esperadas

## 🎓 Conceitos Demonstrados

- **Engenharia de prompts progressiva**: Do básico ao avançado
- **Aplicação prática real**: Sistema completo de análise
- **Comparação de técnicas**: Mesmo input, diferentes resultados
- **Pipeline de processamento**: LangChain para orquestração
- **Validação e estruturação**: Saídas confiáveis
- **Interface de usuário**: Streamlit para acessibilidade

## 🔗 Integração com outros módulos

- **02-frameworks**: Usa LangChain para orquestração
- **04-RAG**: Preparação para sistemas de recuperação
- **05-memory**: Base para sistemas com memória
- **06-MCP-A2A**: Prompts como ferramentas para agentes