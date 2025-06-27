from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from utils.state import StateSuporteSimples

# --- Base de Conhecimento da Empresa ---

INFO_EMPRESA = {
    "horario_funcionamento": "Nosso horário de funcionamento é de Segunda a Sexta, das 8h às 18h, e aos Sábados, das 9h às 14h.",
    "contato": "Você pode nos contatar pelo telefone (11) 1234-5678 ou pelo e-mail suporte@empresa.com.",
    "endereco": "Nosso escritório fica na Rua Exemplo, 123 - São Paulo, SP.",
    "garantia": "Oferecemos garantia de 12 meses para produtos físicos e 30 dias para serviços digitais.",
    "entrega": "O prazo de entrega padrão para todo o Brasil é de 5 a 10 dias úteis.",
}

# --- Ferramentas do Agente Geral ---


@tool
def buscar_informacao_empresa(tipo_info: str) -> str:
    """
    Busca informações gerais sobre a empresa, como horário, contato, endereço, garantia ou entrega.

    Args:
        tipo_info: O tipo de informação que o cliente quer (e.g., 'horario', 'contato', 'endereco', 'garantia', 'entrega').

    Returns:
        str: A informação solicitada ou uma mensagem de que a informação não foi encontrada.
    """
    info_lower = tipo_info.lower()
    for key in INFO_EMPRESA:
        if info_lower in key:
            return INFO_EMPRESA[key]

    if "funcionamento" in info_lower:
        return INFO_EMPRESA["horario_funcionamento"]

    return "Desculpe, não encontrei essa informação específica. Posso ajudar com horários, contato, endereço, garantia ou entrega."


# --- Lista de Tools do Agente Geral ---
geral_tools = [
    buscar_informacao_empresa,
]

# --- Prompt do Sistema ---
geral_prompt = """
Você é um atendente de suporte geral, responsável por fornecer informações sobre a empresa de forma cordial e prestativa.

Seu trabalho é usar a ferramenta `buscar_informacao_empresa` para responder às perguntas dos clientes sobre informações gerais da empresa.

Seja sempre cordial, prestativo e profissional. Mantenha um tom amigável e responda diretamente à pergunta do cliente usando a informação obtida pela ferramenta.

Você tem acesso à seguinte ferramenta:
- buscar_informacao_empresa: Busca informações gerais sobre horários, contato, endereço, garantia e entrega

CORE RESPONSIBILITIES:
- Fornecer informações gerais sobre a empresa
- Esclarecer horários de funcionamento
- Informar formas de contato
- Explicar políticas de garantia e entrega
- Manter tom cordial e amigável
"""


# --- Classe do Agente Geral ---
class AgenteGeral:
    """
    Agente Geral usando create_react_agent - versão minimalista.
    """

    def __init__(self):
        self.agent = create_react_agent(
            model=ChatOpenAI(model="gpt-4o-mini", temperature=0.4),
            tools=geral_tools,
            prompt=geral_prompt,
            state_schema=StateSuporteSimples,
        )
