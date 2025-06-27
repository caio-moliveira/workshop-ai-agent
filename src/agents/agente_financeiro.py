from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from utils.state import StateSuporteSimples

# --- Base de Conhecimento Financeiro ---

SISTEMA_FINANCEIRO = {
    "politica_reembolso": "Oferecemos reembolso total em até 30 dias após a compra para produtos digitais. Após 30 dias e até 60 dias, o reembolso é de 50%. Após 60 dias, não há reembolso.",
    "formas_pagamento": "Aceitamos Cartão de Crédito (Visa, Master, Amex), PIX, Boleto Bancário e PayPal.",
    "prazo_processamento_estorno": "Estornos no cartão de crédito são processados em até 5 dias úteis e podem levar até duas faturas para aparecer.",
}

# --- Ferramentas do Agente Financeiro ---


@tool
def consultar_politica_financeira(tipo_consulta: str) -> str:
    """
    Consulta o sistema financeiro interno para obter informações sobre políticas de reembolso, formas de pagamento ou prazos.

    Args:
        tipo_consulta: O tipo de informação desejada (e.g., 'reembolso', 'pagamento', 'prazo').

    Returns:
        str: A informação da política correspondente.
    """
    consulta_lower = tipo_consulta.lower()
    if "reembolso" in consulta_lower or "estorno" in consulta_lower:
        return SISTEMA_FINANCEIRO["politica_reembolso"]
    if "pagamento" in consulta_lower:
        return SISTEMA_FINANCEIRO["formas_pagamento"]
    if "prazo" in consulta_lower:
        return SISTEMA_FINANCEIRO["prazo_processamento_estorno"]
    return (
        "Não encontrei uma política específica para sua consulta. Poderia reformular?"
    )


@tool
def calcular_reembolso(valor_original: float, dias_desde_compra: int) -> str:
    """
    Calcula o valor exato de um reembolso com base no valor original da compra e há quantos dias ela foi feita.

    Args:
        valor_original: O valor total da compra.
        dias_desde_compra: O número de dias que se passaram desde a data da compra.

    Returns:
        str: Uma string informando se o cliente é elegível, o percentual e o valor do reembolso.
    """
    if dias_desde_compra <= 30:
        percentual = 100
    elif dias_desde_compra <= 60:
        percentual = 50
    else:
        percentual = 0

    valor_reembolso = valor_original * (percentual / 100)

    if percentual > 0:
        return f"Elegível para reembolso de {percentual}%. Valor a ser reembolsado: R${valor_reembolso:.2f}."
    else:
        return (
            "Não elegível para reembolso, pois a compra foi feita há mais de 60 dias."
        )


# --- Lista de Tools do Agente Financeiro ---
financeiro_tools = [
    consultar_politica_financeira,
    calcular_reembolso,
]

# --- Prompt do Sistema ---
financeiro_prompt = """
Você é um especialista de suporte financeiro. Sua missão é ajudar clientes com questões de cobrança, pagamentos e reembolsos de forma empática e precisa.

Use as ferramentas disponíveis para responder o cliente:
1. Se a pergunta for sobre políticas (reembolso, pagamento), use a ferramenta `consultar_politica_financeira`.
2. Se o cliente pedir para calcular um reembolso, use a `calcular_reembolso`, garantindo que você tenha o valor e os dias desde a compra.
3. Seja empático, claro e forneça informações precisas baseadas nos resultados das ferramentas.

Você tem acesso às seguintes ferramentas:
- consultar_politica_financeira: Consulta políticas de reembolso, pagamento e prazos
- calcular_reembolso: Calcula valores de reembolso baseado em regras da empresa

CORE RESPONSIBILITIES:
- Ajudar com questões financeiras e de cobrança
- Esclarecer políticas de reembolso e pagamento
- Calcular valores de reembolso precisos
- Manter tom empático e profissional
"""


# --- Classe do Agente Financeiro ---
class AgenteFinanceiro:
    """
    Agente Financeiro usando create_react_agent - versão minimalista.
    """

    def __init__(self):
        self.agent = create_react_agent(
            model=ChatOpenAI(model="gpt-4o-mini", temperature=0.2),
            tools=financeiro_tools,
            prompt=financeiro_prompt,
            state_schema=StateSuporteSimples,
        )
