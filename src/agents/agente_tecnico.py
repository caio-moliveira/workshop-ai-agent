from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from utils.state import StateSuporteSimples

# --- Base de Conhecimento Técnico ---

KNOWLEDGE_BASE_TECNICO = {
    "login": "Verifique se o email e a senha estão corretos e tente redefinir a senha através do link 'Esqueci minha senha'.",
    "conexao": "Reinicie seu modem e roteador. Verifique também se outros dispositivos na mesma rede estão funcionando.",
    "erro": "Tente limpar o cache e os cookies do seu navegador e recarregar a página. Se o erro persistir, nos informe o código do erro.",
    "lentidao": "Feche outros programas ou abas do navegador que não esteja usando e verifique o uso de CPU no gerenciador de tarefas.",
}

# --- Ferramentas do Agente Técnico ---


@tool
def buscar_solucao_tecnica(problema: str) -> str:
    """
    Busca uma solução para um problema técnico na base de conhecimento interna.

    Args:
        problema: Uma descrição do problema técnico do cliente (e.g., 'login', 'conexao', 'erro', 'lentidao').

    Returns:
        str: A solução encontrada na base de conhecimento ou uma mensagem indicando que nada foi encontrado.
    """
    problema_lower = problema.lower()
    for keyword, solucao in KNOWLEDGE_BASE_TECNICO.items():
        if keyword in problema_lower:
            return f"Solução encontrada: {solucao}"
    return "Nenhuma solução específica encontrada na base de conhecimento. Por favor, descreva o problema com mais detalhes."


@tool
def avaliar_complexidade_tecnica(query: str) -> str:
    """
    Avalia se um problema técnico é muito complexo e precisa ser escalado para um especialista de nível 2.

    Args:
        query: A consulta completa do cliente.

    Returns:
        str: Retorna 'escalate' se for complexo, ou 'continue' caso contrário.
    """
    palavras_complexas = [
        "sistema travou",
        "erro crítico",
        "dados perdidos",
        "servidor",
        "banco de dados",
    ]
    query_lower = query.lower()
    if any(palavra in query_lower for palavra in palavras_complexas):
        return "escalate"
    return "continue"


# --- Lista de Tools do Agente Técnico ---
tecnico_tools = [
    buscar_solucao_tecnica,
    avaliar_complexidade_tecnica,
]

# --- Prompt do Sistema ---
tecnico_prompt = """
Você é um especialista em suporte técnico. Seu objetivo é resolver problemas dos clientes de forma eficiente e clara.

Siga estes passos:
1. Primeiro, use a ferramenta `buscar_solucao_tecnica` para ver se existe uma solução pronta na base de conhecimento.
2. Se uma solução for encontrada, apresente-a ao cliente de forma clara e em formato passo-a-passo.
3. Use a ferramenta `avaliar_complexidade_tecnica` para verificar se o problema é crítico. Se o resultado for 'escalate', informe ao cliente que o problema será encaminhado para um especialista de nível 2.
4. Responda sempre de forma técnica, mas acessível.

Você tem acesso às seguintes ferramentas:
- buscar_solucao_tecnica: Busca soluções na base de conhecimento técnico
- avaliar_complexidade_tecnica: Avalia se o problema precisa ser escalado

CORE RESPONSIBILITIES:
- Resolver problemas técnicos dos clientes
- Fornecer soluções passo-a-passo claras
- Identificar problemas complexos que precisam de escalação
- Manter tom profissional e acessível
"""


# --- Classe do Agente Técnico ---
class AgenteTecnico:
    """
    Agente Técnico usando create_react_agent - versão minimalista.
    """

    def __init__(self):
        self.agent = create_react_agent(
            model=ChatOpenAI(model="gpt-4o-mini", temperature=0.3),
            tools=tecnico_tools,
            prompt=tecnico_prompt,
            state_schema=StateSuporteSimples,
        )
